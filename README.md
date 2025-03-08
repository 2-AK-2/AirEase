# AirEase: Smart Wearable Cooling Device

## 🚀 Overview
AirEase is a wearable device designed to manage **palmar hyperhidrosis** using **Peltier Effect Cooling** and multi-sensor integration. The device syncs with a mobile app to provide **personalized cooling** based on sensor inputs and **AI-driven predictions**.

---

## 📊 Market Potential & Scalability

### **Market Size**
- **Global Wearable Cooling Market**: $10.88B (2024), projected to reach **$17.35B by 2030** (CAGR: 8%).
- **Target Segments**:
  - Individuals with **hyperhidrosis** (~390M people).
  - **Athletes** (~200M people).
  - **Professionals in high-stress jobs** (~100M people).
- **Total Addressable Market (TAM)**: ~690M potential users worldwide.

### **Scalability Plan**
1. **Initial Focus**: Hyperhidrosis patients & athletes.
2. **Expansion**: Corporate wellness programs, healthcare applications.
3. **Distribution Strategy**: E-commerce platforms, direct-to-consumer sales, and partnerships.

---

## 💰 Price Point & Implementation

### **Production Cost per Unit**
| Component               | Cost (USD) |
|------------------------|------------|
| GSR Sensor            | Rs.700        |
| LM35 Temperature Sensor | Rs.400        |
| Heart Rate Sensor     | Rs.300        |
| Peltier Module        | Rs.250        |
| Piezo Fan        | Rs.1500         |
| Power Unit (Battery) | Rs.1200        |
| Micro-controller    | Rs.700        |
| Casing & Assembly    | Rs.1500        |
| **Total Cost**       | **Rs.6550**    |

---

## 🛠️ Sensor Threshold Detection Code (C++ for Arduino)
```cpp
const int GSR_PIN = A0;
const int TEMP_PIN = A1;
const int HEART_RATE_PIN = A2;

int gsrThreshold = 500; // Moisture detection level
float tempThreshold = 37.5; // Body temperature threshold (°C)
int heartRateThreshold = 100; // BPM threshold for increased stress

void setup() {
    Serial.begin(9600);
}

void loop() {
    int gsrValue = analogRead(GSR_PIN);
    float tempValue = (analogRead(TEMP_PIN) * 5.0 / 1023.0) * 100.0;
    int heartRate = analogRead(HEART_RATE_PIN); // Simulated heart rate reading

    if (gsrValue > gsrThreshold || tempValue > tempThreshold || heartRate > heartRateThreshold) {
        Serial.println("Sweat detected! Activating cooling system...");
        // Activate cooling system (Peltier & Fan control logic here)
    }
    delay(1000);
}
```

---

## 🌬️ AI-Powered Cooling Prediction Model
The AI model predicts **when cooling should activate** based on past sensor data trends. It utilizes:

- **Machine Learning** (Regression & Classification Models).
- **Historical User Data & Sensor Inputs**.
- **Real-Time Monitoring**.

### **Key Features**
✔ Predicts when sweating is likely based on past patterns.
✔ Adjusts airflow dynamically (more cooling during peak stress hours).
✔ Self-learns from user responses to improve accuracy.

---

## 📅 Google Calendar Integration for Smart Cooling
AirEase syncs with **Google Calendar** to activate cooling during high-priority events.

### **Steps**:
1. Extract event importance & time slots using **Google Calendar API**.
2. Trigger AI model to preemptively **cool based on upcoming tasks**.
3. Set **airflow duration** based on event length & stress level prediction.

### **Example Implementation (Python with Google API)**
```python
from googleapiclient.discovery import build
import datetime

def get_calendar_events():
    service = build('calendar', 'v3', credentials=CREDENTIALS)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

for event in get_calendar_events():
    if "important" in event['summary'].lower():
        print(f"Trigger cooling for event: {event['summary']} at {event['start']['dateTime']}")
```

---

## 🧘 Meditation Breath Analysis (Heart Rate-Based)
AirEase provides **haptic feedback vibrations** for guided breathing:
✔ **Slow vibrations** when heart rate is high.
✔ **Gentle pulsations** to guide inhale/exhale cycles.

### **Implementation (Arduino)**
```cpp
const int VIBRATION_MOTOR = 9;
void guidedBreathing(int bpm) {
    int inhaleDuration = map(bpm, 60, 120, 4000, 2000); // Map HR to breath cycle
    int exhaleDuration = inhaleDuration;
    
    analogWrite(VIBRATION_MOTOR, 150);
    delay(inhaleDuration);
    analogWrite(VIBRATION_MOTOR, 0);
    delay(exhaleDuration);
}
```

---

## 🔗 Future Enhancements
✅ **Edge AI Integration** for Faster Predictions.
✅ **Smart Cooling Adjustments** via **Weather API**.
✅ **Multi-User Adaptability** for Personalized Comfort.

---

## 🏆 Contributors
- **Khushi Mahesh** – Founder, AirEase
- **Khushi Bhupesh** - Product Development
- **Akshaya Krishna M** - Tech Lead

📬 Contact: ** **

---

## "Stay Cool, Stay Confident – AirEase." 🚀
