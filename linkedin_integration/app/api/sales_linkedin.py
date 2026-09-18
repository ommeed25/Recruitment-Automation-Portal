from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..db.dependencies import get_db
from ..services.linkedin_service import get_user_info
from ..services.sales_linkedin_db_service import save_sales_linkedin_account
from ..services.sales_linkedin_oauth_service import (
    exchange_sales_code_for_token,
    get_sales_authorization_url,
)


router = APIRouter(
    prefix="/sales/auth/linkedin",
    tags=["Sales LinkedIn"]
)


@router.get("/authorize")
def authorize_sales_linkedin(email: str):
    return RedirectResponse(
        get_sales_authorization_url(email)
    )


@router.get("/callback")
def callback_sales_linkedin(
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    token = exchange_sales_code_for_token(code)
    user = get_user_info(token["access_token"])

    account = save_sales_linkedin_account(
        db=db,
        email=state,
        token=token,
        user=user
    )

    return {
        "message": "Sales LinkedIn account saved successfully",
        "account_id": account.id
    }
