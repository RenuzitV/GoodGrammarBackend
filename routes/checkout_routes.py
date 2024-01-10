from flask import request, Blueprint, abort

from middleware.clerk_middleware import token_required
from services.checkout_service import create_checkout
from utils.exceptions import UserNotFoundError, UserDoesNotHaveStripeIdError
from utils.token_utils import get_user_id

bp = Blueprint('checkout', __name__)


@bp.route('/', methods=['POST'])
@token_required
def create_checkout_session(token):
    """
    Creates a checkout session for a user. Requires a `price_id` in the request body and
    the decorative function `token_required` to retrieve the user information.

    :param token: The user's token from the token_required decorator
    """
    user_id = get_user_id(token)
    data = request.get_json()
    if data['price_id'] is None:
        abort(400, "Price ID is required")

    try:
        create_checkout(user_id, data['price_id'])
    except UserNotFoundError:
        print("could not get user ", user_id, " to create checkout")
        abort(404, "User not found")
    except UserDoesNotHaveStripeIdError:
        print("User ", user_id, " does not have a Stripe ID")
        abort(403, "User does not have a Stripe ID")
    except Exception as e:
        print("Error: ", e)
        abort(500, "Internal Server Error")
