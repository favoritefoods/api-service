import os
from typing import Optional
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    MapAttribute,
    ListAttribute,
)


class FavoriteFood(MapAttribute):
    id: NumberAttribute = NumberAttribute(default=0)
    name: UnicodeAttribute = UnicodeAttribute(default="")


class DbUser(Model):
    class Meta:
        table_name: str = "User"
        host: Optional[str] = os.environ.get("AWS_DYNAMODB_HOST")

    username: UnicodeAttribute = UnicodeAttribute(hash_key=True, default="")
    first_name: UnicodeAttribute = UnicodeAttribute(default="")
    last_name: UnicodeAttribute = UnicodeAttribute(default="")
    email: UnicodeAttribute = UnicodeAttribute(default="")
    password: UnicodeAttribute = UnicodeAttribute(default="")
    id: UnicodeAttribute = UnicodeAttribute(default="")
    favorite_foods: ListAttribute = ListAttribute(of=FavoriteFood, default=[])
    friends: ListAttribute = ListAttribute(of=UnicodeAttribute, default=[])
