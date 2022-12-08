
from django.conf import settings
import requests


def get_account_id_by_username(username: str):
    try:
        response = requests.get("https://api.lamadava.com/v1/user/by/username", params={
            "username": username
        }, headers={
            "accept": "application/json",
            "x-access-key": settings.LAMADAVA_API_KEY
        }, timeout=30)
    except:
        return {}

    try:
        return response.json()
    except:
        return {}


def user_is_following(username: str, username_2: str):
    username_id = get_account_id_by_username(username).get("pk")

    if username_id == None:
        return {"detail": "usernotfound"}

    try:
        response = requests.get("https://api.lamadava.com/v1/user/search/followers", params={
            "user_id": username_id,
            "query": username_2
        }, headers={
            "accept": "application/json",
            "x-access-key": settings.LAMADAVA_API_KEY
        }, timeout=30)
    except:
        return []

    try:
        return response.json()
    except:
        return []