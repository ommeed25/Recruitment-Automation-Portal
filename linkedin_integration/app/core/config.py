import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
LINKEDIN_SALES_REDIRECT_URI = os.getenv("LINKEDIN_SALES_REDIRECT_URI")
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
DATABASE_URL = os.getenv("DATABASE_URL")
ORDS_URL=os.getenv("ORDS_URL")

