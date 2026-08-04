# LinkedIn Integration

A FastAPI-based application for LinkedIn OAuth authentication and API integration.

## Features

- LinkedIn OAuth 2.0 login flow
- Token exchange via authorization code
- Environment-based configuration

## Project Structure

```
linkedin-integration/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── utils/
│   ├── scheduler/
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
├── .env
└── README.md
```

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env`
3. Run the app: `uvicorn app.main:app --reload`

## Endpoints

- `GET /` — Home endpoint
- `GET /login` — Initiates LinkedIn OAuth flow
- `GET /auth/linkedin/callback` — OAuth callback handler