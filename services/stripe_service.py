import os
from typing import List

import stripe
from dotenv import load_dotenv
from stripe import Subscription, ListObject

from models.user_model import User
from services import user_service
from utils.exceptions import UserDoesNotHaveStripeIdError, UserAlreadyHasSubscriptionError, UserNotFoundError, \
    InternalServerError, NoActiveSubscriptionError
from models.subscription_tier_model import SubscriptionTier

load_dotenv()


def get_stripe_customer(customer_id):
    return stripe.Customer.retrieve(customer_id)


def get_active_subscriptions(user: User) -> ListObject[Subscription]:
    if user.get_stripe_id is None:
        raise UserDoesNotHaveStripeIdError("User does not have a Stripe ID")

    try:
        user_subscriptions = stripe.Subscription.list(
            customer=user.get_stripe_id(),
            status='active'
        )
        return user_subscriptions
    except Exception as e:
        print("Error when retrieving user subscriptions: ", e)
        raise e


def create_checkout(user_id, price_id):
    user = user_service.get_user(user_id)

    active_subscriptions = get_active_subscriptions(user)
    if len(active_subscriptions) > 0:
        print("User already has an active subscription, redirecting to billing portal")
        return get_stripe_customer_portal_session(user_id)

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
    print("handling new subscription")
    customer_id = data['customer']
    subscription_id = data['id']

    user = user_service.get_user_by_stripe_id(customer_id)
    if not user:
        print("user not found")
        return

    subscriptions = get_active_subscriptions(user)

    if len(subscriptions) > 1:
        print("user already has a subscription, cancelling old subscriptions")

    for subscription in subscriptions:
        if subscription.id != subscription_id:
            subscription.cancel()


def get_stripe_customer_portal_session(user_id):
    user = User.objects(clerk_id=user_id).first()
    if not user:
        raise UserNotFoundError("User not found")

    if not user.stripe_id:
        raise InternalServerError("User does not have a Stripe ID")

    customer_id = user.stripe_id

    return stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=os.getenv("BILLING_PORTAL_RETURN_URL")
    )


def change_subscription(user_id, price_id):
    user = user_service.get_user(user_id)

    active_subscriptions = get_active_subscriptions(user)

    latest_subscription: Subscription = max(active_subscriptions, key=lambda sub: sub.created)

    # if the user has more than one active subscription, cancel the old ones
    if len(active_subscriptions) > 1:
        print("User already has an active subscription, cancelling old subscriptions")
        for subscription in active_subscriptions:
            if subscription.id != latest_subscription.id:
                subscription.cancel()

    subscription_items = stripe.SubscriptionItem.list(
        subscription=latest_subscription.id
    )

    if len(subscription_items) > 1:
        print("User has more than one subscription item, which is not supposed to happen")
        for subscription_item in subscription_items:
            if subscription_item.id != subscription_items.data[0].id:
                stripe.SubscriptionItem.delete(subscription_item.id)

    try:
        stripe.Subscription.modify(
            id=latest_subscription.id,
            cancel_at_period_end=False,
            items=[{
                'id': subscription_items.data[0].id,
                'price': price_id,
            }]
        )
        return latest_subscription
    except Exception as e:
        print("Error when creating a subscription: ", e)
        raise e


def get_customer_subscribe_item_id(user_id):
    user = user_service.get_user(user_id)

    active_subscriptions = get_active_subscriptions(user)

    if len(active_subscriptions) == 0:
        raise NoActiveSubscriptionError("User does not have an active subscription")

    subscription_items = stripe.SubscriptionItem.list(
        subscription=active_subscriptions.data[0].id
    )

    return subscription_items.data[0].price.id


# def check_if_user_has_correct_subscription(user_id, subscription_tier: SubscriptionTier):
#     user = user_service.get_user(user_id)
#
#     active_subscriptions = get_active_subscriptions(user)
#
#     if len(active_subscriptions) == 0:
#         raise NoActiveSubscriptionError("User does not have an active subscription")
#
#     if len(active_subscriptions) > 1:
#         print("User has more than one active subscription")
#         raise InternalServerError("User has more than one active subscription")
#
#     subscription_items = stripe.SubscriptionItem.list(
#         subscription=active_subscriptions.data[0].id
#     )
#
#     return subscription_items.data[0].price.id == subscription_tier.value
