import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
)


class DbUser(Model):
    class Meta:
        table_name: str = "User"
        host: str = os.environ.get("AWS_DYNAMODB_HOST")

    username: UnicodeAttribute = UnicodeAttribute(hash_key=True, default="")
    first_name: UnicodeAttribute = UnicodeAttribute(default="")
    last_name: UnicodeAttribute = UnicodeAttribute(default="")
    email: UnicodeAttribute = UnicodeAttribute(default="")
    password: UnicodeAttribute = UnicodeAttribute(default="")
    id: UnicodeAttribute = UnicodeAttribute(default="")
