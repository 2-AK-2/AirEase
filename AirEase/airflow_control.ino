#include <TensorFlowLite.h>
#include "airflow_model.h"  // Pretrained model deployed as TensorFlow Lite format

#define GSR_PIN A0
#define TEMP_PIN A1
#define HEARTBEAT_PIN 2
#define FAN_SPEED_PIN 9  // PWM control for airflow adjustment

float gsr, temperature, bpm;

// Load model
TfLiteTensor* input_tensor;
TfLiteTensor* output_tensor;
tflite::MicroInterpreter interpreter(model);

// Setup
void setup() {
    Serial.begin(9600);
    pinMode(FAN_SPEED_PIN, OUTPUT);
}

// Loop
void loop() {
    // Read sensor values
    gsr = analogRead(GSR_PIN);
    temperature = (analogRead(TEMP_PIN) * 5.0 / 1023.0) * 100.0;
    bpm = readHeartRate();

    // Prepare input for AI model
    float input_data[3] = {gsr, temperature, bpm};
    input_tensor->data.f = input_data;

    // Run inference
    interpreter.Invoke();
    int airflow_level = output_tensor->data.f[0];  // AI prediction

    // Control fan based on AI prediction
    adjustFanSpeed(airflow_level);

    Serial.print("AI Predicted Airflow: ");
    Serial.println(airflow_level);

    delay(1000);
}

// Adjust fan speed dynamically
void adjustFanSpeed(int level) {
    int pwmValue = (level == 0) ? 0 : (level == 1) ? 128 : 255;  // Low, Medium, High
    analogWrite(FAN_SPEED_PIN, pwmValue);
}

// Simulated heart rate function
int readHeartRate() {
    int pulseCount = 0;
    unsigned long startTime = millis();
    while (millis() - startTime < 1000) {
        if (digitalRead(HEARTBEAT_PIN) == HIGH) {
            pulseCount++;
            delay(100);
        }
    }
    return pulseCount * 6;
}
