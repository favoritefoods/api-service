# Base Tutorial: https://pynamodb.readthedocs.io/en/stable/tutorial.html
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute,
)
from datetime import datetime


def my_default_value() -> str:
    return "My default value"


# Table definition
class Thread(Model):
    class Meta:
        table_name: str = "Thread"
        host: str = "http://localhost:4566"  # LocalStack server

    forum_name: UnicodeAttribute = UnicodeAttribute(
        hash_key=True, default=my_default_value
    )
    subject: UnicodeAttribute = UnicodeAttribute(range_key=True, default="no subject")
    views: NumberAttribute = NumberAttribute(default=0)
    replies: NumberAttribute = NumberAttribute(default=0)
    answered: NumberAttribute = NumberAttribute(default=0)
    tags: UnicodeSetAttribute = UnicodeSetAttribute(null=True)
    # attribute will be called "lpdt" in DynamoDB to save space
    last_post_datetime: UTCDateTimeAttribute = UTCDateTimeAttribute(
        null=True, attr_name="lpdt"
    )


# Create
if not Thread.exists():
    Thread.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
thread_item: Thread = Thread("forum_name", "forum_subject")
thread_item.save()


def test_table():
    # Read
    assert Thread.exists()
    thread_item = Thread.get("forum_name", "forum_subject")  # O(1) time complexity
    assert thread_item.forum_name == "forum_name"
    assert thread_item.subject == "forum_subject"
    assert thread_item.views == 0  # default value
    assert not thread_item.tags  # nullable
    assert not thread_item.last_post_datetime  # nullable

    # Update
    thread_item.update(
        actions=[
            Thread.views.set(Thread.views + 1),
            Thread.last_post_datetime.set(datetime.now()),
        ]
    )
    assert thread_item.forum_name == "forum_name"
    assert thread_item.subject == "forum_subject"
    assert thread_item.views == 1  # updated
    assert not thread_item.tags
    assert thread_item.last_post_datetime  # updated


# Delete
def test_delete_item():
    thread_item.delete()
    try:
        Thread.get("forum_name", "forum_subject")
    except Exception as does_not_exist:
        assert does_not_exist


def test_delete_table():
    Thread.delete_table()
    assert not Thread.exists()
