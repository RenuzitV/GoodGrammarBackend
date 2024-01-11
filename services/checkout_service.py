from services import user_service
from utils.exceptions import UserDoesNotHaveStripeIdError
import stripe


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
            allow_promotion_codes=True,
            payment_method_collection="if_required",
            mode='subscription',
            success_url='https://www.youtube.com/watch?v=ufbOHl1mmYk&pp=ygUKaGFwcHkgc29uZw%3D%3D',
            cancel_url='https://www.youtube.com/watch?v=EZEfN5z8Mlg',
        )
        print("successfully created checkout session: ", checkout_session.id)
        return checkout_session.url
    except Exception as e:
        print("Error when creating a checkout session: ", e)
        raise e
