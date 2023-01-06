# coding: utf-8

from typing import Dict, List, Union, Tuple

from fastapi.testclient import TestClient

from unittest.mock import patch

from httpx import Response

from openapi_server.models.list_restaurants import ListRestaurants  # noqa: F401
from openapi_server.models.list_reviews import ListReviews  # noqa: F401
from openapi_server.main import app


@patch(
    "httpx.AsyncClient.get",
    return_value=Response(
        200,
        json={
            "html_attributions": [],
            "results": [
                {
                    "business_status": "OPERATIONAL",
                    "geometry": {
                        "location": {"lat": 40.7546795, "lng": -73.9870291},
                        "viewport": {
                            "northeast": {
                                "lat": 40.75601118029149,
                                "lng": -73.98556926970849,
                            },
                            "southwest": {
                                "lat": 40.7533132197085,
                                "lng": -73.9882672302915,
                            },
                        },
                    },
                    "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png",
                    "icon_background_color": "#FF9E67",
                    "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet",
                    "name": "Joe's Pizza Broadway",
                    "opening_hours": {"open_now": True},
                    "photos": [
                        {
                            "height": 9000,
                            "html_attributions": [
                                '<a href="https://maps.google.com/maps/contrib/102814344397000225596">Marlene Escobar</a>'
                            ],
                            "photo_reference": "ARywPAKhaV30O5tIjdrNQU4F9rxRqjbJ_deUxPouP-ieg05kgg_vySCuY2OzkbTBkE-3gftdXk213f2wyjK2RlHXjUiG0kziHarrSfXk6KYD7B9ZIt_MTxrp03V0DgxJbaLhnbeUStBjCgfVxGKzsqEsechd8_YPwUdB-p9S3yrWZzRss3MT",
                            "width": 12000,
                        }
                    ],
                    "place_id": "ChIJifIePKtZwokRVZ-UdRGkZzs",
                    "plus_code": {
                        "compound_code": "Q237+V5 New York, NY, USA",
                        "global_code": "87G8Q237+V5",
                    },
                    "price_level": 1,
                    "rating": 4.5,
                    "reference": "ChIJifIePKtZwokRVZ-UdRGkZzs",
                    "scope": "GOOGLE",
                    "types": [
                        "meal_delivery",
                        "restaurant",
                        "food",
                        "point_of_interest",
                        "establishment",
                    ],
                    "user_ratings_total": 13538,
                    "vicinity": "1435 Broadway, New York",
                }
            ],
            "status": "OK",
        },
    ),
)
def test_get_restaurants(client: TestClient):
    """Test case for get_restaurants

    Find restaurants in user location given
    """
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")

    params: List[Tuple[str, Union[str, int, float, bool, None]]] = [
        ("latitude", 40.7546795),
        ("longitude", -73.9870291),
        ("radius", 25),
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
                "id": "ChIJifIePKtZwokRVZ-UdRGkZzs",
                "name": "Joe's Pizza Broadway",
                "latitude": 40.7546795,
                "longitude": -73.9870291,
                "address": "1435 Broadway, New York",
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
        "/restaurants/{restaurantId}/reviews".format(
            restaurantId="restaurant_id_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
