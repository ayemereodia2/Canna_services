# pylint: disable=import-error
import logging
from typing import Any, Dict, TypedDict

import requests
from django.urls import reverse
from pydantic import EmailStr, HttpUrl

from cannassaince.settings import FacebookSettings, GeneralSettings

from .models import CustomUser

ERROR_MESSAGE = "access_denied"

logger = logging.getLogger(__name__)


class OAuthErrorException(Exception):
    pass


class Facebook:
    GET_ACCESS_TOKEN_ERROR = "Failed to obtain access token from Facebook."
    GET_USER_INFO_ERROR = "Failed to obtain user info from Facebook."

    @classmethod
    def get_facebook_access_token(cls, code: str) -> str:
        """Returns the Facebook access token."""
        data = {
            "code": code,
            "client_id": FacebookSettings().FACEBOOK_APP_ID,
            "client_secret": FacebookSettings().FACEBOOK_SECRET,
            "state": {"{st=state123abc,ds=123456789}"},
        }
        response = requests.post(
            FacebookSettings().FACEBOOK_OAUTH_ACCESS_TOKEN, data=data
        )

        if not response.ok:
            logger.error("An error occured getting access token from facebook")
            raise OAuthErrorException(cls.GET_ACCESS_TOKEN_ERROR)

        access_token = response.json()["access_token"]

        return access_token

    @classmethod
    def get_facebook_user_info(cls, access_token: str) -> Dict[str, Any]:
        """Get the Facebook user's info."""
        response = requests.get(
            FacebookSettings().FACEBOOK_ACCESS_TOKEN,
            params={"access_token": access_token, "fields": "id,name,email"},
        )
        if not response.ok:
            logger.error("An error occured getting user info from facebook")
            raise OAuthErrorException(cls.GET_USER_INFO_ERROR)

        return response.json()


def normalize_username(name: str) -> str:
    """Changes the name of the Facebook user to a username."""
    username = []
    for char in name:
        if char.isalpha():
            username.append(char)
    return "".join(username).lower()


def name_to_username(name: str) -> str:
    """Validates the username of the Facebook user."""
    user_name = normalize_username(name)
    if CustomUser.objects.filter(username=user_name).exists():
        usernames = CustomUser.objects.filter(
            username__startswith=user_name
        ).values("username")
        usernames = [username["username"] for username in usernames]
        usernames.sort(reverse=True)
        for username in usernames:
            ending = str(username).lstrip(user_name)
            if ending.isdigit():
                ending = int(ending)
                ending += 1
                return user_name + str(ending)
        return user_name + "1"
    return user_name
