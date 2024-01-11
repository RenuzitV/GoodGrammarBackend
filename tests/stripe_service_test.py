import os
import unittest

from dotenv import load_dotenv

from services import stripe_service, user_service

from database.db import initialize_db

from init_stripe import init_stripe
from services.stripe_service import get_customer_subscribe_item_id

load_dotenv()


class MyTestCase(unittest.TestCase):
    def test_change_subscription(self):
        initialize_db()
        init_stripe.init_stripe()

        price_id_1 = os.getenv("STRIPE_TEST_PRICE_ID_1")
        price_id_2 = os.getenv("STRIPE_TEST_PRICE_ID_2")
        price_id_3 = os.getenv("STRIPE_TEST_PRICE_ID_3")
        clerk_id = os.getenv("CLERK_TEST_USER_ID")

        stripe_service.change_subscription(clerk_id, price_id_1)
        self.assertEqual(get_customer_subscribe_item_id(clerk_id), price_id_1)  # add assertion here
        stripe_service.change_subscription(clerk_id, price_id_2)
        self.assertEqual(get_customer_subscribe_item_id(clerk_id), price_id_2)  # add assertion here
        stripe_service.change_subscription(clerk_id, price_id_3)
        self.assertEqual(get_customer_subscribe_item_id(clerk_id), price_id_3)  # add assertion here


if __name__ == '__main__':
    unittest.main()
