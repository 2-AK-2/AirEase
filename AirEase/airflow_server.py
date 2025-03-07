from flask import Flask, request
import RPi.GPIO as GPIO

app = Flask(__name__)

FAN_PIN = 18  # GPIO pin for fan
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

pwm = GPIO.PWM(FAN_PIN, 100)  # PWM for fan speed
pwm.start(0)

@app.route('/trigger_airflow', methods=['POST'])
def trigger_airflow():
    data = request.get_json()
    level = data.get("level", 0)

    speed = 0 if level == 0 else 50 if level == 1 else 100  # Fan speeds for event importance
    pwm.ChangeDutyCycle(speed)

    return {"status": "success", "speed": speed}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
