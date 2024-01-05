import os

from flask import Flask, request, abort, jsonify, Blueprint
from svix.api import Svix
from svix.exceptions import WebhookVerificationError
from svix.webhooks import Webhook
from services import user_service
from utils.Exceptions import UserAlreadyExistsError, InternalServerError

SVIX_SIGNUP_SECRET = os.getenv("SVIX_SIGNUP_KEY")

bp = Blueprint('clerk', __name__)


@bp.route('/signup', methods=['POST'])
def clerk_webhook():
    # Retrieve the Svix signature from the headers
    headers = request.headers

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    wh = Webhook(SVIX_SIGNUP_SECRET)

    try:
        payload = wh.verify(payload, headers)
        user_id = payload["data"]["id"]

        created_user = user_service.create_user_by_id(user_id)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except InternalServerError:
        abort(500, "Internal Server Error")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, str(e))


@bp.route('/signup_2', methods=['POST'])
def clerk_webhook_no_svix():
    try:
        payload = request.get_json()
        user_id = payload["data"]["id"]

        created_user = user_service.create_user_by_id(user_id)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except InternalServerError:
        abort(500, "Internal Server Error")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, str(e))
