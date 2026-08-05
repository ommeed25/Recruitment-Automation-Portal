from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest
from app.services.auth_service import (
    authenticate,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(request: LoginRequest):

    if not authenticate(
        request.email,
        request.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token()

    return {
        "access_token": token,
        "token_type": "Bearer"
    }