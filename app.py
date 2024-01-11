import os

from flask import Flask
from dotenv import load_dotenv
from routes import auth_routes, user_routes, file_route, stripe_routes
from webhook_routes import clerk_webhook_routes, stripe_webhook_routes

# do NOT remove thí import statement
# it's needed to establish a connection to the database
from database import db

# setup env variables
from init_stripe import init_stripe

load_dotenv()

# initialize database
db = db.initialize_db()

# initialize init_stripe
init_stripe.init_stripe()

# Generate Flask app
app = Flask(__name__)

# register blueprints and add prefix to its routes
app.register_blueprint(auth_routes.bp, url_prefix='/')

app.register_blueprint(clerk_webhook_routes.bp, url_prefix='/webhook/clerk')
app.register_blueprint(stripe_webhook_routes.bp, url_prefix='/webhook/stripe')

app.register_blueprint(user_routes.bp, url_prefix='/user')
app.register_blueprint(file_route.bp, url_prefix='/file')
app.register_blueprint(stripe_routes.bp, url_prefix='/stripe')


# run app if we're on development environment
# otherwise, let the server handle it (e.g. Heroku)
on_dev = os.getenv('FLASK_ENV') != 'production'
if on_dev:
    print("Running on development environment")
    app.run()
else:
    print("Running on production environment, expecting gunicorn to handle it")
