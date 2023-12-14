import os

from flask import Flask, request, abort, jsonify, Blueprint
from svix.api import Svix
from svix.exceptions import WebhookVerificationError
from svix.webhooks import Webhook
from services import user_service

SVIX_SIGNUP_SECRET = os.getenv("SVIX_SIGNUP_KEY")

bp = Blueprint('clerk', __name__)


@bp.route('/signup', methods=['POST'])
def clerk_webhook():
    # Retrieve the Svix signature from the headers
    headers = request.headers

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    try:
        # Verify the signature
        wh = Webhook(SVIX_SIGNUP_SECRET)
        payload = wh.verify(payload, headers)

        # Process the webhook payload here
        # For now, we are not adding the user to our database, just acknowledging the receipt.
        print("Received valid webhook from Clerk")

        user_id = payload["data"]["id"]

        # Create user in our database
        if user_service.create_user_by_id(user_id):
            # Return a response to Clerk
            return jsonify({"status": "ok"}), 200

    except WebhookVerificationError:
        # If the signature verification fails, reject the request
        print("Received invalid webhook from Clerk")
        abort(401)
    except Exception as e:
        print("Received webhook from Clerk but failed to process it")
        print(e)
        abort(500)
