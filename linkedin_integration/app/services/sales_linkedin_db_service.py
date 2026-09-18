from sqlalchemy.orm import Session

from ..db.models import SalesLinkedInAccount


def save_sales_linkedin_account(
    db: Session,
    email: str,
    token: dict,
    user: dict
):
    account = (
        db.query(SalesLinkedInAccount)
        .filter(
            SalesLinkedInAccount.email == email
        )
        .first()
    )

    if account:
        account.linkedin_sub = user["sub"]
        account.full_name = user["name"]

        account.access_token = token["access_token"]
        account.token_type = token["token_type"]
        account.expires_in = token["expires_in"]

    else:
        account = SalesLinkedInAccount(
            employee_id=None,
            linkedin_sub=user["sub"],
            full_name=user["name"],
            email=email,
            access_token=token["access_token"],
            token_type=token["token_type"],
            expires_in=token["expires_in"]
        )

        db.add(account)

    db.commit()
    db.refresh(account)

    return account
