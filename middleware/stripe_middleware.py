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
