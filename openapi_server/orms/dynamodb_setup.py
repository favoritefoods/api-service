from openapi_server.orms.user import DbUser
from openapi_server.orms.review import DbReview
from openapi_server.orms.restaurant import DbRestaurant


def dynamodb_setup():
    if not DbUser.exists():
        DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not DbReview.exists():
        DbReview.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not DbRestaurant.exists():
        DbRestaurant.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
