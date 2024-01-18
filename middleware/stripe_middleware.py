import os
from functools import wraps
from typing import Any

from dotenv import load_dotenv
from flask import request, jsonify, abort
import stripe
from models.subscription_tier_model import SubscriptionTier
from services import user_service, stripe_service
from utils.exceptions import InternalServerError

from utils.token_utils import get_user_id, validate_token

load_dotenv()

# defines the API_KEY once when the server starts
api_key = os.getenv("CLERK_API_KEY")


def authentication_and_subscription_required(required_tier: SubscriptionTier):
    """
    Decorator that checks if the user is authenticated and has the required subscription tier.

    Can be either `SubscriptionTier.Novice` or
    `SubscriptionTier.Expert`.

    Novice is lower than Expert.
    :param required_tier: The required subscription tier.
    """
    def decorator(f):
        # noinspection DuplicatedCode
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            data, error_response = validate_token(token)
            if error_response:
                return {
                    "message": error_response["message"]
                }, error_response["status"]

            user_id = get_user_id(data)

            user = user_service.get_user(user_id)

            try:
                user_has_subscription = stripe_service.check_user_has_access_based_on_tier(user, required_tier)
            except InternalServerError:
                return {
                    "message": "Internal Server Error"
                }, 500

            if not user_has_subscription:
                return {
                    "message": "User does not have the required subscription tier",
                }, 403

            # Proceed with the original function
            return f(data, *args, **kwargs)

        return decorated_function

    return decorator


def authentication_and_subscription_threshold_required(s):
    """
    Decorator that checks if the user is authenticated and their subscription tier can has not reached the upload threshold.
    """
    def decorator(f):
        # noinspection DuplicatedCode
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            data, error_response = validate_token(token)
            if error_response:
                return {
                    "message": error_response["message"]
                }, error_response["status"]

            user_id = get_user_id(data)

            user = user_service.get_user(user_id)

            try:
                user_has_subscription = stripe_service.check_user_has_access_based_on_tier(user, required_tier)
            except InternalServerError:
                return {
                    "message": "Internal Server Error"
                }, 500

            if not user_has_subscription:
                return {
                    "message": "User does not have the required subscription tier",
                }, 403

            # Proceed with the original function
            return f(data, *args, **kwargs)

        return decorated_function

    return decorator
