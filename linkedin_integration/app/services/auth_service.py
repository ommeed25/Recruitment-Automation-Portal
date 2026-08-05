import os
from datetime import datetime, timedelta, UTC

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

def authenticate(email: str, password: str):

    if email != ADMIN_EMAIL:
        return False

    return bcrypt.checkpw(
        password.encode(),
        ADMIN_PASSWORD_HASH.encode()
    )

def create_access_token():

    payload = {
        "sub": ADMIN_EMAIL,
        "exp": datetime.now(UTC)
        + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )