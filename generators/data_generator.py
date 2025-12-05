from faker import Faker
import random
from typing import Dict, Any, List

class UserDataGenerator:
    def __init__(self, locale: str = "en_US"):
        self.fake = Faker(locale)
        self.user_statuses = [0, 1, 2, 3]
