# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.list_restaurants import ListRestaurants  # noqa: F401
from openapi_server.models.list_reviews import ListReviews  # noqa: F401


def test_get_restaurants(client: TestClient):
    """Test case for get_restaurants

    Find restaurants in user location given
    """
    params = [("longitude", 3.4),     ("latitude", 3.4),     ("radius", 56)]
    headers = {
    }
    response = client.request(
        "GET",
        "/restaurants",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_review_by_restaurant(client: TestClient):
    """Test case for get_review_by_restaurant

    Find reviews by restaurant
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/restaurants/{restaurantId}/reviews".format(restaurantId=56),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

