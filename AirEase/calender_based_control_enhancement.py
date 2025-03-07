from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import joblib
import requests  # To send airflow triggers

# Load AI model (previously trained)
model = joblib.load("airflow_model.pkl")

# Authenticate Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

# Get upcoming events
now = datetime.datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

# Define event importance based on keywords
important_keywords = ["meeting", "presentation", "exam", "deadline"]
moderate_keywords = ["workout", "call", "appointment"]

def classify_event(event):
    title = event['summary'].lower()
    if any(word in title for word in important_keywords):
        return 2  # High priority event (strong cooling)
    elif any(word in title for word in moderate_keywords):
        return 1  # Medium priority event (moderate cooling)
    return 0  # Low priority (no cooling)

# Process events
for event in events:
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    event_importance = classify_event(event)

    print(f"Event: {event['summary']} | Importance: {event_importance} | Time: {start_time}")

    # Send trigger to Arduino (or Raspberry Pi)
    if event_importance > 0:
        requests.post("http://raspberrypi.local:5000/trigger_airflow", json={"level": event_importance})
