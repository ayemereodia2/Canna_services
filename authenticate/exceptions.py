from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidFacebookLink(APIException):
    """Exception for invalid Facebook link."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = (
        "The facebook link is invalid. Provide a valid Facebook profile link."
    )
    default_code = "invalid_facebook_link"