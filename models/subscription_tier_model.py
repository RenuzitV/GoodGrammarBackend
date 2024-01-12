import enum
import os

from dotenv import load_dotenv

load_dotenv()


class SubscriptionTier(enum.Enum):
    Novice = "1"
    Expert = "2"

    @property
    def price_ids(self):
        return self.value
