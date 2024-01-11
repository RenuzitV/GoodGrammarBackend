from flask import request, Blueprint, abort, jsonify

import services.stripe_service as stripe_service
from middleware.clerk_middleware import token_required
from utils.exceptions import UserNotFoundError, UserDoesNotHaveStripeIdError, UserAlreadyHasSubscriptionError
from utils.token_utils import get_user_id
from middleware.stripe_middleware import subscription_required
from models.subscription_tier_model import SubscriptionTier

bp = Blueprint('checkout', __name__)


@bp.route('/checkout', methods=['POST'])
@token_required
def create_checkout_session(token):
    """
    Creates a checkout session for a user. Requires a `price_id` in the request body and
    the decorative function `token_required` to retrieve the user information.

    :param token: The user's token from the token_required decorator. This is a MUST-HAVE parameter.
    """
    user_id = get_user_id(token)
    data = request.get_json()
    if data['price_id'] is None:
        abort(400, "Price ID is required")

    try:
        checkout_session_url = stripe_service.create_checkout(user_id, data['price_id'])
        return jsonify({"url": checkout_session_url}), 200
    except UserNotFoundError:
        print("could not get user", user_id, "to create checkout")
        abort(404, "User not found")
    except UserDoesNotHaveStripeIdError:
        print("User", user_id, "does not have a Stripe ID")
        abort(403, "User does not have a Stripe ID")
    except UserAlreadyHasSubscriptionError:
        print("User", user_id, "already has a subscription")
        abort(403, "User already has a subscription")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('/change_subscription', methods=['POST'])
@token_required
def change_customer_subscription(token):
    """
    Changes a customer's subscription. Requires a `price_id` in the request body and
    the decorative function `token_required` to retrieve the user information.

    :param token: The user's token from the token_required decorator. This is a MUST-HAVE parameter.
    """
    user_id = get_user_id(token)
    data = request.get_json()
    if data['price_id'] is None:
        abort(400, "Price ID is required")

    try:
        subscription = stripe_service.change_subscription(user_id, data['price_id'])
        return jsonify({"subscription": subscription}), 200
    except UserNotFoundError:
        print("could not get user", user_id, "to change subscription")
        abort(404, "User not found")
    except UserDoesNotHaveStripeIdError:
        print("User", user_id, "does not have a Stripe ID")
        abort(403, "User does not have a Stripe ID")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('/stripe_portal', methods=['POST'])
@token_required
def get_stripe_portal_url(token):
    user_id = get_user_id(token)
    if not user_id:
        abort(400, "User id is required")

    try:
        customer_portal_url = stripe_service.get_stripe_customer_portal_session(user_id)
        return jsonify({
            "url": customer_portal_url.url
        }), 200
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")


@bp.route('/test_subscription_required', methods=['GET'])
@token_required
@subscription_required(SubscriptionTier.Expert)
def test_subscription_required(token):
    return jsonify({"message": token['sub']}), 200
