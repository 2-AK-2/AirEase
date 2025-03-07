from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import joblib
import requests  # To send airflow triggers
import time
import logging

#Setup Logging for Debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#Load AI Model
model = joblib.load("airflow_model.pkl")

#Authenticate Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

#Define Keywords for Event Classification
IMPORTANT_KEYWORDS = ["meeting", "presentation", "exam", "deadline"]
MODERATE_KEYWORDS = ["workout", "call", "appointment"]

#Function to Classify Event Importance
def classify_event(event):
    title = event.get('summary', "").lower()
    if any(word in title for word in IMPORTANT_KEYWORDS):
        return 2  # High priority event (strong cooling)
    elif any(word in title for word in MODERATE_KEYWORDS):
        return 1  # Medium priority event (moderate cooling)
    return 0  # Low priority (no cooling)

#Function to Get Upcoming Events (Efficient Processing)
def fetch_calendar_events():
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10,
            singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])
    except Exception as e:
        logging.error(f"Google Calendar API error: {e}")
        return []

#Function to Send Airflow Trigger to Raspberry Pi
def trigger_airflow(level):
    try:
        response = requests.post(
            "http://raspberrypi.local:5000/trigger_airflow",
            json={"level": level}, timeout=3
        )
        if response.status_code == 200:
            logging.info(f"Airflow triggered successfully: Level {level}")
        else:
            logging.warning(f"Failed to trigger airflow: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send request to Raspberry Pi: {e}")

#Main Function to Process Events and Adjust Airflow
def main():
    events = fetch_calendar_events()
    if not events:
        logging.info("No upcoming events found.")
        return

    highest_importance = 0  # Track the most important event for cooling level
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        event_importance = classify_event(event)
        logging.info(f"Event: {event['summary']} | Importance: {event_importance} | Time: {start_time}")

        # Update highest importance level
        highest_importance = max(highest_importance, event_importance)

    #Only trigger cooling if needed
    if highest_importance > 0:
        trigger_airflow(highest_importance)

if __name__ == "__main__":
    main()
