from flask import request, Blueprint, json, abort, jsonify
import stripe

bp = Blueprint('stripe', __name__)


@app.route('/webhook', methods=['POST'])
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
        handle_new_subscription(event.data.object)

    return jsonify({'ok', 200})
