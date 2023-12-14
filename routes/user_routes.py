from flask import Blueprint, request

from services import user_service

bp = Blueprint('user', __name__)


@bp.route('/', methods=['POST'])
def create_user():
    return user_service.create_user(request.form)


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return user_service.get_user(user_id)


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_service.delete_user(user_id)
