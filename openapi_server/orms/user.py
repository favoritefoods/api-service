from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
)


class DbUser(Model):
    class Meta:
        table_name: str = "User"
        host: str = "http://host.docker.internal:4566"
        aws_access_key_id: str = "foo"
        aws_secret_access_key: str = "bar"

    username: UnicodeAttribute = UnicodeAttribute(hash_key=True, default="")
    first_name: UnicodeAttribute = UnicodeAttribute(default="")
    last_name: UnicodeAttribute = UnicodeAttribute(default="")
    email: UnicodeAttribute = UnicodeAttribute(default="")
    password: UnicodeAttribute = UnicodeAttribute(default="")
