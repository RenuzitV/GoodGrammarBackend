import stripe
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


def init_stripe():
    stripe.api_key = os.getenv("STRIPE_API_KEY", "")
