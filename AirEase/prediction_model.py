import pandas as pd  
import numpy as np  
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier  
import joblib  

# Load sensor data
data = pd.read_csv("sensor_readings.csv")  # Ensure CSV has GSR, Temp, BPM, Airflow_Label

# Features and labels
X = data[['GSR', 'Temperature', 'BPM']]
y = data['Airflow_Label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model for deployment
joblib.dump(model, "airflow_model.pkl")
