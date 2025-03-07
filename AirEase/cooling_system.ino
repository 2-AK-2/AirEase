//Feed in manual values (for crossing a certain threshold for sensors)
#define GSR_PIN A0       // GSR sensor connected to analog pin A0
#define TEMP_PIN A1      // LM35 temperature sensor connected to analog pin A1
#define HEARTBEAT_PIN 2  // Heartbeat sensor connected to digital pin 2
#define COOLING_PIN 9    // Output pin to activate cooling mechanism

const int gsrThreshold = 100;       // Adjust threshold for sweat detection
const float tempThreshold = 35.0;   // Adjust threshold for body temperature (Celsius)
const int bpmThreshold = 100;       // Adjust threshold for heart rate

int gsrValue = 0;
float temperature = 0.0;
int bpm = 0;

void setup() {
    Serial.begin(9600);
    pinMode(HEARTBEAT_PIN, INPUT);
    pinMode(COOLING_PIN, OUTPUT);
}

void loop() {
    // Read GSR sensor value
    gsrValue = analogRead(GSR_PIN);
    
    // Read temperature sensor (LM35: 10mV per degree Celsius)
    int tempRaw = analogRead(TEMP_PIN);
    temperature = (tempRaw * 5.0 / 1023.0) * 100.0;
    
    // Read heartbeat sensor (basic approach, needs proper BPM calculation)
    bpm = readHeartRate();
    
    Serial.print("GSR: "); Serial.print(gsrValue);
    Serial.print(" | Temp: "); Serial.print(temperature);
    Serial.print("°C | BPM: "); Serial.println(bpm);
    
    // Check if any parameter crosses the threshold
    if (gsrValue > gsrThreshold || temperature > tempThreshold || bpm > bpmThreshold) {
        activateCooling();
    } else {
        deactivateCooling();
    }
    
    delay(1000);
}

// Function to read heart rate (basic pulse detection, should be improved with a proper algorithm)
int readHeartRate() {
    int pulseCount = 0;
    unsigned long startTime = millis();
    while (millis() - startTime < 1000) { // Count pulses in 1 second
        if (digitalRead(HEARTBEAT_PIN) == HIGH) {
            pulseCount++;
            delay(100); // Basic debounce (adjust as needed)
        }
    }
    return pulseCount * 6; // Convert to BPM (approximation)
}

// Function to activate cooling system
void activateCooling() {
    digitalWrite(COOLING_PIN, HIGH);
    Serial.println("Cooling activated!");
}

// Function to deactivate cooling system
void deactivateCooling() {
    digitalWrite(COOLING_PIN, LOW);
    Serial.println("Cooling deactivated.");
}
