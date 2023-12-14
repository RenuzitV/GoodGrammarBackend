from models.user_model import User
from flask import Blueprint, jsonify


bp = Blueprint('user', __name__)


@bp.route('/', methods=['POST'])
def create_user():
    return User().create_user()


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return User().get_user(user_id)


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return User().delete_user(user_id)
