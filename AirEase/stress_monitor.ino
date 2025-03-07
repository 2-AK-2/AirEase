#include <Wire.h>
#include <Adafruit_MLX90614.h>  // Temperature sensor (if needed)
#include <MAX30105.h>           // Heart rate sensor
#include <Arduino.h>

MAX30105 particleSensor;
int BPM;  // Heart rate
int vibrationPin = 9;  // Vibration motor

// Stress detection threshold (adjustable)
int stressThreshold = 90;  // If BPM > 90, initiate guided breathing

void setup() {
    Serial.begin(115200);
    pinMode(vibrationPin, OUTPUT);

    if (!particleSensor.begin()) {
        Serial.println("Heart Rate Sensor not found!");
        while (1);
    }
    Serial.println("Heart Rate Sensor Initialized.");
}

void loop() {
    BPM = getHeartRate();  // Function to measure BPM

    Serial.print("Heart Rate: ");
    Serial.println(BPM);

    // If BPM exceeds threshold, start meditation mode
    if (BPM > stressThreshold) {
        Serial.println("High stress detected! Starting breath guidance...");
        guidedBreathing();
    }
    
    delay(2000);  // Check every 2 sec
}

// Function to measure heart rate
int getHeartRate() {
    long irValue = particleSensor.getIR();  // Get IR value
    return map(irValue, 50000, 120000, 60, 120);  // Convert to BPM
}

// Function to trigger guided breathing with vibrations
void guidedBreathing() {
    for (int i = 0; i < 3; i++) {  // Run 3 breath cycles
        Serial.println("Inhale...");
        analogWrite(vibrationPin, 150);  // Strong vibration
        delay(4000);  // 4-sec inhale

        Serial.println("Hold...");
        analogWrite(vibrationPin, 50);   // Gentle pulse
        delay(2000);  // 2-sec hold

        Serial.println("Exhale...");
        analogWrite(vibrationPin, 80);   // Slow fade vibration
        delay(6000);  // 6-sec exhale

        analogWrite(vibrationPin, 0);    // Stop vibration
        delay(2000);  // Rest before next cycle
    }

    Serial.println("Breathing session complete.");
}
