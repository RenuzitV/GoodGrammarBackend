import os
from functools import wraps

from dotenv import load_dotenv
from jose import jwt
from flask import request, abort
import requests
from utils.token_utils import validate_token

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

        data, error_response = validate_token(token)
        if error_response:
            return {
                "message": error_response["message"]
            }, error_response["status"]

        return f(data, *args, **kwargs)

    return decorated
