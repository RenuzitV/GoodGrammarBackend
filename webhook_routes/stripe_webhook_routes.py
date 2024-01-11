import os

from flask import request, Blueprint, json, abort, jsonify
import stripe
import services.stripe_service as stripe_service

bp = Blueprint('stripe', __name__)

endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')


@bp.route('/', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        abort(400, 'Invalid payload')
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        abort(400, 'Invalid signature')

    # Handle the event
    if event and event.type == 'customer.subscription.created':
        stripe_service.handle_new_subscription(event.data.object)

    return jsonify({'ok', 200})
