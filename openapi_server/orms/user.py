import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
)


class DbUser(Model):
    class Meta:
        table_name: str = "User"
        host: str = os.environ.get("AWS_DYNAMODB_HOST")
        aws_access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY")

    username: UnicodeAttribute = UnicodeAttribute(hash_key=True, default="")
    first_name: UnicodeAttribute = UnicodeAttribute(default="")
    last_name: UnicodeAttribute = UnicodeAttribute(default="")
    email: UnicodeAttribute = UnicodeAttribute(default="")
    password: UnicodeAttribute = UnicodeAttribute(default="")
