from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.orm import Session

from ..db.dependencies import get_db
from ..services.linkedin_db_service import save_linkedin_account

from ..db.models import Job, LinkedInAccount
from app.services.linkedin_service import build_linkedin_payload,publish_post

from datetime import datetime

from app.db.models import LinkedInPost
from app.services.linkedin_publish_service import publish_job_service

from ..services.linkedin_service import (   
    get_authorization_url,
    exchange_code_for_token,
    get_user_info,
)

router = APIRouter(
    prefix="/auth/linkedin",
    tags=["LinkedIn"]
)




@router.get("/authorize")
def authorize(email: str):
    return RedirectResponse(
        get_authorization_url(email)
    )


@router.get("/callback")
def callback(
    code: str,
    state: str,
    db: Session = Depends(get_db)
    ):
    token = exchange_code_for_token(code)

    user = get_user_info(token["access_token"])

    account = save_linkedin_account(
    db=db,
    email=state,
    token=token,
    user=user
    )

    return {
        "message": "LinkedIn account saved successfully",
        "account_id": account.id
    }


@router.get("/payload/{job_id}")
def preview_linkedin_payload(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.job_id == job_id)
        .first()
    )

    if not job:
        return {"message": "Job not found"}

    linkedin_account = (
        db.query(LinkedInAccount)
        .first()
    )

    if not linkedin_account:
        return {"message": "LinkedIn account not found"}

    return build_linkedin_payload(
        job,
        linkedin_account
    )


   
@router.post("/publish/{job_id}")
def publish_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    return publish_job_service(job_id, db)