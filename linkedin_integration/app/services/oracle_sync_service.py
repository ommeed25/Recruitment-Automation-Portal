from requests import get
from decouple import config


ORDS_URL = config("ORDS_URL")


def fetch_jobs():
    response = get(ORDS_URL)
    response.raise_for_status()
    return response.json()["items"]
