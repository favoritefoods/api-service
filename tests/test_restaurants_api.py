# coding: utf-8

from typing import Dict, List, Union, Tuple

from fastapi.testclient import TestClient


from openapi_server.models.list_restaurants import ListRestaurants  # noqa: F401
from openapi_server.models.list_reviews import ListReviews  # noqa: F401
from openapi_server.main import app


def test_get_restaurants(client: TestClient):
    """Test case for get_restaurants

    Find restaurants in user location given
    """
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")

    params: List[Tuple[str, Union[str, int, float, bool, None]]] = [
        ("latitude", 40.7675),
        ("longitude", -73.832764),
        ("radius", 125),
    ]
    headers: Dict = {}
    response = client.request(
        "GET",
        "restaurants",
        headers=headers,
        params=params,
    )

    assert response.status_code == 200
    assert response.json() == {
        "restaurants": [
            {
                "id": "ChIJS1mNV6yKwokRgBOlGbotUIk",
                "name": "New 88",
                "latitude": 40.7666602,
                "longitude": -73.83243499999999,
                "address": "33-05 Farrington Street, Queens",
            }
        ],
    }


def test_get_review_by_restaurant(client: TestClient):
    """Test case for get_review_by_restaurant

    Find reviews by restaurant
    """

    headers = {}
    response = client.request(
        "GET",
        "/restaurants/{restaurantId}/reviews".format(restaurantId=56),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
