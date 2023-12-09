from flask import Flask, jsonify

from middleware.auth_middleware import token_required


def create_app():
    """
    Create app
    add blueprints here to register them as routes
    :return: app
    """
    app = Flask(__name__)

    from routes import auth

    # register blueprints and add prefix to its routes
    app.register_blueprint(auth.bp, url_prefix='/')

    return app


if __name__ == '__main__':
    create_app().run()
