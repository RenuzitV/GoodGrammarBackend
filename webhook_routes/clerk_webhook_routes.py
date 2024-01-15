import os

from flask import request, abort, jsonify, Blueprint
from svix.exceptions import WebhookVerificationError
from svix.webhooks import Webhook

from services import user_service
from utils.exceptions import UserAlreadyExistsError

SVIX_SIGNUP_SECRET = os.getenv("SVIX_SIGNUP_KEY")
SVIX_DELETE_SECRET = os.getenv("SVIX_DELETE_KEY")
SVIX_UPDATE_SECRET = os.getenv("SVIX_UPDATE_KEY")

bp = Blueprint('clerk', __name__)


def get_user_info_from_payload(payload):
    user_id = payload["data"]["id"]
    user_primary_email_id = payload["data"]["primary_email_address_id"]
    user_first_name = payload["data"]["first_name"]
    user_last_name = payload["data"]["last_name"]

    user_name = ""

    if user_first_name is not None:
        user_name += user_first_name

    if user_name != "" and user_last_name is not None:
        user_name += " " + user_last_name
    elif user_name == "" and user_last_name is not None:
        user_name = user_last_name

    if user_name == "":
        user_name = "John Doe"

    user_email = user_service.get_user_email(user_primary_email_id)
    return user_id, user_email, user_name


@bp.route('/signup', methods=['POST'])
def clerk_webhook():
    # Retrieve the Svix signature from the headers
    headers = request.headers

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    wh = Webhook(SVIX_SIGNUP_SECRET)

    try:
        payload = wh.verify(payload, headers)

        user_id, user_email, user_name = get_user_info_from_payload(payload)

        created_user = user_service.create_user(user_id, user_email, user_name)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, "Internal Server Error")


@bp.route('/delete', methods=['POST'])
def clerk_webhook_delete():
    # Retrieve the Svix signature from the headers
    headers = request.headers

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    wh = Webhook(SVIX_DELETE_SECRET)

    try:
        payload = wh.verify(payload, headers)
        user_id = payload["data"]["id"]

        deleted_user = user_service.delete_user(user_id)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, "Internal Server Error")


@bp.route('/update', methods=['POST'])
def clerk_webhook_update():
    # Retrieve the Svix signature from the headers
    headers = request.headers

    # Retrieve the request body as a raw string
    payload = request.get_data(as_text=True)

    wh = Webhook(SVIX_UPDATE_SECRET)

    try:
        payload = wh.verify(payload, headers)
        user_id = payload["data"]["id"]

        updated_user = user_service.update_user(user_id)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, "Internal Server Error")


@bp.route('/signup_2', methods=['POST'])
def clerk_webhook_no_svix():
    try:
        payload = request.get_json()

        user_id, user_email, user_name = get_user_info_from_payload(payload)

        created_user = user_service.create_user(user_id, user_email, user_name)
        return jsonify({"status": "ok"}), 200

    except UserAlreadyExistsError:
        return abort(409, "User already exists")

    except WebhookVerificationError:
        print("Invalid Webhook signature from Clerk")
        abort(401, "Invalid Webhook signature from Clerk")

    except Exception as e:
        print("Failed to process webhook:", e)
        abort(500, "Internal Server Error")
