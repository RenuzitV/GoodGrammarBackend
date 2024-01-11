"""
    this file is purely for testing purposes
    it is not part of the main project
"""
import os

from dotenv import load_dotenv
import stripe
from stripe import Subscription, ListObject

load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')
customer = stripe.Customer.retrieve(os.getenv("TEST_CUSTOMER_ID"), expand=["subscriptions"])
# print(customer)
subscriptions = customer.subscriptions.data
filtered = filter(lambda subscription: subscription.status == "active", subscriptions)
active_subscriptions = list(filtered)
print(active_subscriptions)
