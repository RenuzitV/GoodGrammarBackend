import os

from dotenv import load_dotenv

from services import user_service
from utils.exceptions import UserDoesNotHaveStripeIdError, UserAlreadyHasSubscriptionError
import stripe

load_dotenv()


def get_active_subscriptions(user_id):
    user = user_service.get_user(user_id)
    if user.get_stripe_id is None:
        raise UserDoesNotHaveStripeIdError("User does not have a Stripe ID")

    user_subscriptions = stripe.Customer.retrieve(user.get_stripe_id(), expand=["subscriptions"]).subscriptions.data
    active_subscriptions = list(filter(lambda subscription: subscription.status == "active", user_subscriptions))
    return active_subscriptions


def create_checkout(user_id, price_id):
    active_subscriptions = get_active_subscriptions(user_id)
    if len(active_subscriptions) > 0:
        raise UserAlreadyHasSubscriptionError("User already has an active subscription")

    try:
        checkout_session = stripe.checkout.Session.create(
            customer=user.get_stripe_id(),  # Customer's Stripe ID
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,  # Subscription Price ID
                'quantity': 1,
            }],
            allow_promotion_codes=True,
            payment_method_collection="if_required",
            mode='subscription',
            success_url=os.getenv('STRIPE_SUCCESS_URL'),
            cancel_url=os.getenv('STRIPE_CANCEL_URL'),
        )
        print("successfully created checkout session: ", checkout_session.id)
        return checkout_session.url
    except Exception as e:
        print("Error when creating a checkout session: ", e)
        raise e


def handle_new_subscription(data):
    return None