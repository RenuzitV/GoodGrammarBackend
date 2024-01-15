from jwt import InvalidTokenError

from services.clerk_service import decode_jwt
from jose import jwt

from utils.exceptions import NoBearerTokenError


def get_user_id(token) -> str:
    return token["sub"]


def validate_token(token):
    if not token:
        return None, {"message": "Token is missing!", "status": 400}
    try:
        data = decode_jwt(token)
        return data, None
    except jwt.ExpiredSignatureError:
        return None, {"message": "Token is expired!", "status": 401}
    except (jwt.JWTClaimsError, jwt.JWTError, InvalidTokenError):
        return None, {"message": "Token is invalid!", "status": 401}
    except NoBearerTokenError:
        return None, {"message": "Token is missing!", "status": 401}
    except Exception as e:
        print("error 500 while validating token:\n", e)
        return None, {"message": "Something went wrong", "status": 500}
