from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import pickle
from typing import List, Dict, Any

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """Handle Google Calendar authentication."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_upcoming_meetings(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Fetch upcoming meetings from Google Calendar."""
        if not self.service:
            self.authenticate()

        now = datetime.utcnow().isoformat() + 'Z'
        end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def get_meeting_details(self, meeting_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific meeting."""
        if not self.service:
            self.authenticate()

        try:
            event = self.service.events().get(
                calendarId='primary',
                eventId=meeting_id
            ).execute()
            return event
        except Exception as e:
            raise Exception(f"Failed to fetch meeting details: {str(e)}")

    def extract_participants(self, event: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract participant information from a calendar event."""
        participants = []
        
        # Get attendees from the event
        attendees = event.get('attendees', [])
        for attendee in attendees:
            if attendee.get('email') != event.get('creator', {}).get('email'):
                participants.append({
                    'email': attendee.get('email'),
                    'name': attendee.get('displayName', ''),
                    'response_status': attendee.get('responseStatus', 'needsAction')
                })
        
        return participants 