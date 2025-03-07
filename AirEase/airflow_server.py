from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import threading
import time

app = Flask(__name__)

FAN_PIN = 18  # GPIO pin for fan
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

pwm = GPIO.PWM(FAN_PIN, 100)  # 100Hz PWM for smooth control
pwm.start(0)  # Initially off

# ✅ Smoothly adjust fan speed instead of abrupt jumps
def adjust_fan_speed(target_speed):
    global current_speed
    step = 5  # Adjust speed in small increments
    while abs(current_speed - target_speed) > step:
        current_speed += step if current_speed < target_speed else -step
        pwm.ChangeDutyCycle(current_speed)
        time.sleep(0.2)  # Gradual change every 200ms
    pwm.ChangeDutyCycle(target_speed)  # Final set speed

@app.route('/trigger_airflow', methods=['POST'])
def trigger_airflow():
    global current_speed
    data = request.get_json()
    level = data.get("level", 0)

    # ✅ Fan Speed Mapping
    speed_map = {0: 0, 1: 50, 2: 100}
    target_speed = speed_map.get(level, 0)

    # ✅ Run fan adjustment in a separate thread
    threading.Thread(target=adjust_fan_speed, args=(target_speed,)).start()

    return jsonify({"status": "success", "speed": target_speed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
