import requests
import json
import time

# ✅ OpenWeather API Configuration
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "65d8bfaa75447dc71fef7a5c95ca9c4f"  # Ensure no extra spaces/newlines
CITY = "London"  # Change to your city
DEVICE_URL = "http://raspberrypi.local:5000/trigger_airflow"  # Raspberry Pi API URL

# ✅ Define cooling thresholds (adjust as needed)
TEMP_THRESHOLD = 30  # Celsius - Sweating starts ~30°C
HUMIDITY_THRESHOLD = 70  # % - High humidity increases sweating

def get_weather():
    """Fetches real-time weather data from OpenWeather API."""
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP failures

        weather_data = response.json()
        if 'main' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            return temp, humidity
        else:
            print(f"⚠️ API Error: {weather_data}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network/API Error: {e}")
        return None, None

def determine_airflow(temp, humidity):
    """Determines cooling level based on temperature & humidity."""
    if temp > TEMP_THRESHOLD and humidity > HUMIDITY_THRESHOLD:
        return 2, "🚀 Airflow ON at HIGH level 🌀🔥"
    elif temp > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
        return 1, "🔄 Airflow ON at MODERATE level 🌬️"
    else:
        return 0, "❄️ Airflow OFF"

def send_airflow_command(level, message):
    """Sends cooling adjustment command to Raspberry Pi/Arduino."""
    payload = {"level": level}

    try:
        response = requests.post(DEVICE_URL, json=payload)
        response.raise_for_status()  # Raise an error for HTTP failures
        print(f"✅ {message}")  # Print the airflow status
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Failed to send airflow command: {e}")

def main():
    while True:
        temp, humidity = get_weather()

        if temp is not None and humidity is not None:
            print(f"🌡️ Current Weather: {temp}°C, {humidity}% Humidity")

            airflow_level, message = determine_airflow(temp, humidity)
            send_airflow_command(airflow_level, message)

        time.sleep(1800)  # Refresh every 30 minutes

if __name__ == "__main__":
    main()
