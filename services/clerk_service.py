# decorative functions seems to need to call load_dotenv() again? not sure why
import os

import requests
from dotenv import load_dotenv
from flask import abort
from jose import jwt
from jwt import InvalidTokenError

from utils.exceptions import *

load_dotenv()

# defines the API_KEY once when the server starts
api_key = os.getenv("CLERK_API_KEY")


def get_jwks(bearer_token):
    # noinspection GrazieInspection
    """
        Get JWKS from Clerk API
        :param bearer_token: Clerk API Key from .env file
        :return: JWKS as JSON array of possible keys
        """
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.get('https://api.clerk.com/v1/jwks', headers=headers)
    return response.json()


def decode_jwt(token):
    """
    Decode JWT token
    Requires `CLERK_API_KEY` to be set in .env file
    :param token: JWT token
    :return: decoded JWT token
    """
    if not api_key:
        print("Clerk API Key is missing!")
        raise NoBearerTokenError("Clerk API Key is missing!")

    jwks = get_jwks(api_key)

    header = jwt.get_unverified_header(token)

    # basically finds the key with the same kid as the token for us to decode
    key = [k for k in jwks['keys'] if k["kid"] == header["kid"]]

    # check if key has at least one element
    if not key:
        print("Invalid token")
        raise InvalidTokenError("Invalid token")

    key = key[0]

    decoded = jwt.decode(token, key)

    return decoded
