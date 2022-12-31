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
                        "location": {"lat": 40.7666602, "lng": -73.83243499999999},
                        "viewport": {
                            "northeast": {
                                "lat": 40.7680213802915,
                                "lng": -73.83120021970849,
                            },
                            "southwest": {
                                "lat": 40.7653234197085,
                                "lng": -73.8338981802915,
                            },
                        },
                    },
                    "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png",
                    "icon_background_color": "#FF9E67",
                    "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet",
                    "name": "New 88",
                    "opening_hours": {"open_now": False},
                    "photos": [
                        {
                            "height": 2322,
                            "html_attributions": [
                                '<a href="https://maps.google.com/maps/contrib/113190293207555088222">luis fernandez</a>'
                            ],
                            "photo_reference": "ARywPAK8rZ-NNzHXIWqTQhKgx7riuRAa_3L54mYnvwdAWvVj19rd56MCsW5uw0Jpr5VZc94yQ_4CpLRv5loP03cfyDZCkkQONkh77D9rwG8eRJvzw_-OeQwXPDkBVWQftOArGiFV-yheX0QtZBMX8z5uVNOyP0urr3IenuG1kbTaKZ7enGJB",
                            "width": 4128,
                        }
                    ],
                    "place_id": "ChIJS1mNV6yKwokRgBOlGbotUIk",
                    "plus_code": {
                        "compound_code": "Q589+M2 New York, NY, USA",
                        "global_code": "87G8Q589+M2",
                    },
                    "rating": 4.1,
                    "reference": "ChIJS1mNV6yKwokRgBOlGbotUIk",
                    "scope": "GOOGLE",
                    "types": [
                        "restaurant",
                        "food",
                        "point_of_interest",
                        "establishment",
                    ],
                    "user_ratings_total": 8,
                    "vicinity": "33-05 Farrington Street, Queens",
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
        "/restaurants/{restaurantId}/reviews".format(
            restaurantId="restaurant_id_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
