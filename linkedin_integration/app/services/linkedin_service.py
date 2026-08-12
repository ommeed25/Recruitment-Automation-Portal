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

def upload_image_to_linkedin(
    access_token: str,
    image_path: str,
    person_urn: str,
):
    url = "https://api.linkedin.com/rest/images?action=initializeUpload"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202601",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "initializeUploadRequest": {
            "owner": person_urn
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("Image initialization status:", response.status_code)
    print("Image initialization response:", response.text)

    response.raise_for_status()

    data = response.json()

    upload_url = data["value"]["uploadUrl"]
    image_urn = data["value"]["image"]

    with open(image_path, "rb") as image_file:
        upload_response = requests.put(
            upload_url,
            headers={
                "Content-Type": "application/octet-stream"
            },
            data=image_file
        )

    print("Image upload status:", upload_response.status_code)
    print("Image upload response:", upload_response.text)

    upload_response.raise_for_status()

    return image_urn

def publish_vendor_post(
    access_token: str,
    person_urn: str,
    image_urn: str,
    hashtags: list[str],
):
    url = "https://api.linkedin.com/rest/posts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202601",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    hashtag_text = " ".join(hashtags)

    payload = {
        "author": person_urn,
        "commentary": hashtag_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "content": {
            "media": {
                "title": "Vendor Partnership",
                "id": image_urn
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("Vendor post status:", response.status_code)
    print("Vendor post response:", response.text)

    response.raise_for_status()

    return response

