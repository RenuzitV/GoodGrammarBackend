import os
from functools import wraps
from jose import jwt
from flask import request, abort
import requests


def get_jwks(bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.get('https://api.clerk.com/v1/jwks', headers=headers)
    return response.json()


def decode_jwt(token):
    api_key = os.getenv("CLERK_API_KEY")
    if not api_key:
        abort(500, "Clerk API Key is missing!")

    jwks = get_jwks(api_key)

    header = jwt.get_unverified_header(token)

    key = [k for k in jwks['keys'] if k["kid"] == header["kid"]][0]

    decoded = jwt.decode(token, key)

    return decoded


def token_required(f):
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
