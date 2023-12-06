from flask import Flask, jsonify

from middleware.auth_middleware import token_required

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Hello world
    :return: Hello World message
    """
    return 'Hello World!!!'


@app.route('/test_auth')
@token_required
def test_auth(token):
    """
    Test auth
    does not need to check for authorization. if we get here, it means that the token is valid
    :param token: returned token from `token_required`
    :return: authorized message and claims from JWT token
    """

    return jsonify({
        "message": "Authorized",
        "data": token
    }), 200


if __name__ == '__main__':
    app.run()
