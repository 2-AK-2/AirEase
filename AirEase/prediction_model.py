import pandas as pd  
import numpy as np  
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier  
from lightgbm import LGBMClassifier
import joblib  
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Input

# Load sensor data
data = pd.read_csv("sensor_readings.csv")  # Ensure CSV has GSR, Temp, BPM, Airflow_Label

# Features and labels
X = data[['GSR', 'Temperature', 'BPM']]
y = data['Airflow_Label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "airflow_rf_model.pkl")

# Train LightGBM Model
lgbm_model = LGBMClassifier(n_estimators=100)
lgbm_model.fit(X_train, y_train)
joblib.dump(lgbm_model, "airflow_lgbm_model.pkl")

# Train TensorFlow Neural Network Model
tf_model = keras.Sequential([
    Input(shape=(3,)),  # GSR, Temperature, BPM
    Dense(8, activation='relu'),
    Dense(8, activation='relu'),
    Dense(3, activation='softmax')  # 3 classes: No cooling, Moderate, High
])

tf_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
tf_model.fit(X_train, y_train, epochs=50, batch_size=8)

# Convert to TensorFlow Lite for edge deployment
converter = tf.lite.TFLiteConverter.from_keras_model(tf_model)
tflite_model = converter.convert()
with open("airflow_model.tflite", "wb") as f:
    f.write(tflite_model)
