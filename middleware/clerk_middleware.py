import os
from functools import wraps

from dotenv import load_dotenv
from jose import jwt
from flask import request, abort
import requests

# decorative functions seems to need to call load_dotenv() again? not sure why
load_dotenv()

# defines the API_KEY once when the server starts
api_key = os.getenv("CLERK_API_KEY")


def get_jwks(bearer_token):
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
        abort(500, "Something went wrong. Please contact support")

    jwks = get_jwks(api_key)

    header = jwt.get_unverified_header(token)

    # basically finds the key with the same kid as the token for us to decode
    key = [k for k in jwks['keys'] if k["kid"] == header["kid"]]

    # check if key has at least one element
    if not key:
        abort(401, "Invalid Token!")

    key = key[0]

    decoded = jwt.decode(token, key)

    return decoded


def token_required(f):
    """
    Token required decorator.
    Requires the `Authorization` header with JWT token

    :return: if the message is authenticated, the claims from JWT token. Otherwise, an error message in the form of JSON
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                       "message": "Authentication Token is missing!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        try:
            data = decode_jwt(token)
        except jwt.ExpiredSignatureError:
            return {
                       "message": "Token is expired!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        except jwt.JWTClaimsError:
            return {
                       "message": "Token is invalid!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        except jwt.JWTError:
            return {
                       "message": "Token is invalid!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        except Exception as e:
            print("error 500:\n", e)
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500

        return f(data, *args, **kwargs)

    return decorated
