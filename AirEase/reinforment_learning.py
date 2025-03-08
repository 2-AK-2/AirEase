import gym
import numpy as np
import random
from sklearn.preprocessing import StandardScaler
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Create a reinforcement learning environment for AirEase adaptation
class AirEaseEnv(gym.Env):
    def __init__(self, data):
        super(AirEaseEnv, self).__init__()
        
        self.data = data
        self.index = 0

        # Observation space: GSR, Pulse, Temperature
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)

        # Action space: 0 (off), 1 (moderate airflow), 2 (high airflow)
        self.action_space = gym.spaces.Discrete(3)

        # Standardize input data
        self.scaler = StandardScaler()
        self.data[["GSR (Sweat Level)", "Pulse (BPM)", "Body Temperature (°C)"]] = self.scaler.fit_transform(
            self.data[["GSR (Sweat Level)", "Pulse (BPM)", "Body Temperature (°C)"]])

    def reset(self):
        self.index = 0
        return self._get_observation()

    def step(self, action):
        correct_action = self.data.iloc[self.index]["Airflow Level"]

        # Reward function: +1 if correct, -1 if wrong
        reward = 1 if action == correct_action else -1

        self.index += 1
        done = self.index >= len(self.data) - 1

        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        obs = self.data.iloc[self.index][["GSR (Sweat Level)", "Pulse (BPM)", "Body Temperature (°C)"]].values
        return np.array(obs, dtype=np.float32)

# Define Deep Q-Network (DQN)
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # Discount rate
        self.epsilon = 1.0   # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            Dense(24, activation='relu', input_shape=(self.state_size,)),
            Dense(24, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Train the reinforcement learning model
env = AirEaseEnv(pd.DataFrame({
    "GSR (Sweat Level)": gsr_values,
    "Pulse (BPM)": pulse_values,
    "Body Temperature (°C)": body_temperature,
    "Airflow Level": user_activations
}))

state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)

# Training parameters
episodes = 500
batch_size = 32

for e in range(episodes):
    state = env.reset().reshape(1, state_size)
    total_reward = 0

    for time_step in range(len(env.data)):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        next_state = next_state.reshape(1, state_size)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

        if done:
            print(f"Episode {e+1}/{episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
            break

    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

# Save trained model
agent.model.save("reinforcement_airflow_model.h5")

print("Reinforcement Learning Model Training Complete!")
