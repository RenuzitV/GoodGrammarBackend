import os

from flask import Flask, request, abort, jsonify, Blueprint
from svix.api import Svix
from svix.exceptions import WebhookVerificationError
from svix.webhooks import Webhook

SVIX_SIGNUP_SECRET = os.getenv("SVIX_SIGNUP_KEY")

bp = Blueprint('clerk', __name__)


@bp.route('/signup', methods=['POST'])
def clerk_webhook():
    # Retrieve the Svix signature from the headers
    signature = request.headers.get('Svix-Signature')

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    try:
        # Verify the signature
        wh = Webhook(SVIX_SIGNUP_SECRET)
        payload = wh.verify(payload, signature)

        # Process the webhook payload here
        # For now, we are not adding the user to our database, just acknowledging the receipt.
        print("Received valid webhook from Clerk")
        print(payload)

        # Return a response to Clerk
        return jsonify({"status": "ok"}), 200

    except WebhookVerificationError:
        # If the signature verification fails, reject the request
        abort(401)
