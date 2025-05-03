from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Kevin - Meeting Assistant",
    description="Professional meeting preparation assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class MeetingParticipant(BaseModel):
    name: str
    email: str
    linkedin_url: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None

class Meeting(BaseModel):
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    participants: List[MeetingParticipant]
    description: Optional[str] = None
    location: Optional[str] = None
    talking_points: Optional[List[str]] = None

@app.get("/")
async def root():
    return {"message": "Welcome to Kevin - Your Meeting Assistant"}

@app.get("/meetings", response_model=List[Meeting])
async def get_upcoming_meetings():
    """
    Get upcoming meetings from Google Calendar
    """
    # TODO: Implement Google Calendar integration
    return []

@app.get("/meetings/{meeting_id}", response_model=Meeting)
async def get_meeting_details(meeting_id: str):
    """
    Get detailed information about a specific meeting
    """
    # TODO: Implement meeting details retrieval
    raise HTTPException(status_code=404, detail="Meeting not found")

@app.get("/meetings/{meeting_id}/talking-points")
async def get_talking_points(meeting_id: str):
    """
    Generate talking points for a specific meeting
    """
    # TODO: Implement talking points generation
    return {"talking_points": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 