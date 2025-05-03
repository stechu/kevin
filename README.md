# Kevin - Professional Meeting Assistant

Kevin is an intelligent meeting assistant that helps you prepare for your meetings by:
- Syncing with your Google Calendar
- Researching meeting participants using LinkedIn data
- Analyzing organizations and individuals
- Generating relevant talking points

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   APIFY_API_KEY=your_apify_key
   OPENAI_API_KEY=your_openai_key
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Features

- **Calendar Integration**: Automatically syncs with Google Calendar to fetch upcoming meetings
- **Participant Research**: Uses Apify to gather professional information about meeting participants
- **Organization Analysis**: Deep research on companies and organizations
- **Talking Points**: AI-generated relevant discussion points based on participant profiles and meeting context

## Project Structure

```
kevin/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── calendar/            # Google Calendar integration
│   ├── research/            # Research and analysis modules
│   ├── apify/              # LinkedIn data scraping
│   └── ai/                 # AI-powered talking points generation
├── tests/                  # Test files
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Security

- All API keys and sensitive information are stored in environment variables
- OAuth2 authentication for Google Calendar integration
- Secure API key management for third-party services

## Contributing

Feel free to submit issues and enhancement requests! 