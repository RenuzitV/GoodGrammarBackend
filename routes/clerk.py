from flask import Flask, request, abort, jsonify, Blueprint
from svix.api import Svix
from svix.exceptions import WebhookVerificationError

SVIX_SECRET = 'whsec_kIzK2X66hsfeyzH3+F56QHJhzoqmCnej'

bp = Blueprint('clerk', __name__)


@bp.route('/signup', methods=['POST'])
def clerk_webhook():
    # Retrieve the Svix signature from the headers
    signature = request.headers.get('Svix-Signature')

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    try:
        # Verify the signature
        svix = Svix(SVIX_SECRET)
        svix.webhook.verify_signature(payload, signature)

        # Process the webhook payload here
        # For now, we are not adding the user to our database, just acknowledging the receipt.
        print("Received valid webhook from Clerk")

        # Return a response to Clerk
        return jsonify({"status": "ok"}), 200

    except WebhookVerificationError:
        # If the signature verification fails, reject the request
        abort(401)
