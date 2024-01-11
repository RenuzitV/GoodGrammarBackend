import os
from functools import wraps
from typing import Any

from dotenv import load_dotenv
from flask import request, jsonify, abort
import stripe
from models.subscription_tier_model import SubscriptionTier
from services import user_service

from utils.token_utils import get_user_id

load_dotenv()

# defines the API_KEY once when the server starts
api_key = os.getenv("CLERK_API_KEY")


def subscription_required(required_tier: SubscriptionTier):
    def decorator(f):
        @wraps(f)
        def decorated_function(token, *args, **kwargs):
            user_id = get_user_id(token)

            if not user_id:
                return jsonify({"message": "User ID is missing"}), 401

            try:
                user = user_service.get_user(user_id)

                # Fetch user's active subscriptions from Stripe
                subscriptions = stripe.Subscription.list(
                    customer=user.get_stripe_id(),
                    status='active')

                # Get all subscription items from these subscriptions
                subscription_items_lists = [stripe.SubscriptionItem.list(subscription=subscription.id).data for
                                            subscription in subscriptions]

                # Flatten the list of subscription items
                flattened_subscription_items = [item for sublist in subscription_items_lists for item in sublist]

                # Extract the price IDs from the flattened list
                subscription_items_price_ids = [item.price.id for item in flattened_subscription_items]

                # Check if the user does not have any of the required subscription tier's price IDs
                if not any(item in subscription_items_price_ids for item in required_tier.value):
                    return jsonify({"message": "User does not have the required subscription tier"}), 403

            except Exception as e:
                # Handle exceptions (e.g., Stripe API errors, user not found)
                print(e)
                return jsonify({"message": "Internal Server Error"}), 500

            # Proceed with the original function
            return f(token, *args, **kwargs)

        return decorated_function

    return decorator
