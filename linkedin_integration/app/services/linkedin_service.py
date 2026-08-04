import secrets
from urllib.parse import urlencode
from app.services.content_builder_service import build_recruitment_post

import requests

from ..core.config import (
    LINKEDIN_CLIENT_ID,
    LINKEDIN_CLIENT_SECRET,
    LINKEDIN_REDIRECT_URI,
)


def get_authorization_url(email: str):
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email w_member_social",
        "state": email,
    }

    return (
        "https://www.linkedin.com/oauth/v2/authorization?"
        + urlencode(params)
    )


def exchange_code_for_token(code: str):
    url = "https://www.linkedin.com/oauth/v2/accessToken"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
    }

    response = requests.post(url, data=payload)

    print(response.status_code)
    print(response.text)

    return response.json()


def get_user_info(access_token: str):
    url = "https://api.linkedin.com/v2/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    print(response.text)

    return response.json()

def build_linkedin_payload(job, linkedin_account):

    return {
        "author": f"urn:li:person:{linkedin_account.linkedin_sub}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": build_recruitment_post(job)
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }



def publish_post(
    access_token: str,
    payload: dict
):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response