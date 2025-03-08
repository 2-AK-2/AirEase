import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Regenerate synthetic user-specific sensor data
np.random.seed(42)
num_samples = 1000

# Simulated user input: When they manually turn AirEase on/off
user_activations = np.random.choice([0, 1, 2], num_samples, p=[0.4, 0.4, 0.2])  # 0=Off, 1=Moderate, 2=High

# Generate sensor values
gsr_values = np.random.randint(0, 650, num_samples)  # Sweat levels
pulse_values = np.random.randint(60, 150, num_samples)  # BPM
body_temperature = np.random.uniform(35.5, 40.0, num_samples)  # Celsius

# Define feature set and labels
X = pd.DataFrame({
    "GSR (Sweat Level)": gsr_values,
    "Pulse (BPM)": pulse_values,
    "Body Temperature (°C)": body_temperature
})
y = user_activations  # User preferences for airflow

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an optimized RandomForest model with adjusted parameters
best_model = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=5, min_samples_leaf=2, random_state=42)
best_model.fit(X_train, y_train)

# Predict and evaluate
y_pred_optimized = best_model.predict(X_test)
optimized_accuracy = accuracy_score(y_test, y_pred_optimized)

# Save the optimized model
joblib.dump(best_model, "optimized_adaptive_airflow_model.pkl")

# Display new accuracy
optimized_accuracy
