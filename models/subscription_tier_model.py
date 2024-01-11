import enum
import os

from dotenv import load_dotenv

load_dotenv()

class SubscriptionTier(enum.Enum):
    Novice = [os.getenv("PRICE_NOVICE_MONTHLY_ID"), os.getenv("PRICE_NOVICE_YEARLY_ID")]
    Expert = [os.getenv("PRICE_EXPERT_MONTHLY_ID"), os.getenv("PRICE_EXPERT_YEARLY_ID")]

    @property
    def price_ids(self):
        return self.value
