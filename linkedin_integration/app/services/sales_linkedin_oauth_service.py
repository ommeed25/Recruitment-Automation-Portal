from urllib.parse import urlencode

import requests

from ..core.config import (
    LINKEDIN_AUTH_URL,
    LINKEDIN_CLIENT_ID,
    LINKEDIN_CLIENT_SECRET,
    LINKEDIN_SALES_REDIRECT_URI,
)


SALES_LINKEDIN_SCOPE = "openid profile email w_member_social"


def get_sales_authorization_url(email: str):
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_SALES_REDIRECT_URI,
        "scope": SALES_LINKEDIN_SCOPE,
        "state": email,
    }

    return f"{LINKEDIN_AUTH_URL}?{urlencode(params)}"


def exchange_sales_code_for_token(code: str):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "redirect_uri": LINKEDIN_SALES_REDIRECT_URI,
    }

    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=payload
    )

    print(response.status_code)
    print(response.text)

    return response.json()
