import os
from typing import Optional
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
)


class DbRestaurant(Model):
    class Meta:
        table_name: str = "Restaurant"
        host: Optional[str] = os.environ.get("AWS_DYNAMODB_HOST")

    id: UnicodeAttribute = UnicodeAttribute(hash_key=True, default="")
    name: UnicodeAttribute = UnicodeAttribute(default="")
    latitude: NumberAttribute = NumberAttribute(default=0)
    longitude: NumberAttribute = NumberAttribute(default=0)
    address: UnicodeAttribute = UnicodeAttribute(default="")
