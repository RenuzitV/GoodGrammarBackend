from app import stripe
from services import user_service
from utils.exceptions import UserDoesNotHaveStripeIdError


def create_checkout(user_id, price_id):
    user = user_service.get_user(user_id)
    if user.get_stripe_id is None:
        raise UserDoesNotHaveStripeIdError("User does not have a Stripe ID")
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=user.get_stripe_id(),  # Customer's Stripe ID
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,  # Subscription Price ID
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
        )
        return checkout_session.id
    except Exception as e:
        print("Error when creating a checkout session: ", e)
        raise e
