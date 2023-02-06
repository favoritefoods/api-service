# coding: utf-8

from typing import Dict, Tuple
from httpx import Response

from fastapi.testclient import TestClient

from unittest.mock import patch
from moto import mock_dynamodb

from openapi_server.models.api_response import ApiResponse  # noqa: F401
from openapi_server.models.create_review import CreateReview  # noqa: F401
from openapi_server.models.review import Review  # noqa: F401
from openapi_server.models.update_review import UpdateReview  # noqa: F401
from openapi_server.models.user import User
from openapi_server.main import app
from openapi_server.orms.review import DbReview
from openapi_server.orms.user import DbUser
from openapi_server.orms.restaurant import DbRestaurant


def initTestItems() -> Tuple[DbUser, DbRestaurant, DbReview]:
    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    test_user: DbUser = DbUser(
        username="theUser",
        first_name="John",
        last_name="James",
        email="john@email.com",
        password="12345",
        id="1",
    )
    test_user.save()
    assert DbUser.get("theUser").username == "theUser"

    DbRestaurant.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    test_restaurant: DbRestaurant = DbRestaurant(
        id="0",
        name="Joe's Pizza",
        latitude=40.7546795,
        longitude=-73.9870291,
        address="NYC",
    )
    test_restaurant.save()
    assert DbRestaurant.get("0").name == "Joe's Pizza"

    DbReview.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    test_review: DbReview = DbReview(
        id="0",
        created_at="2023",
        updated_at="2023",
        username="theUser",
        restaurant_id="0",
        rating=5,
        favorite_food="pizza",
        starred=True,
        content="Awesome",
        photo_url="www.photouploaded.com",
    )
    test_review.save()
    assert DbReview.get("0").username == "theUser"

    return (test_user, test_restaurant, test_review)


@mock_dynamodb
@patch(
    "httpx.AsyncClient.get",
    return_value=Response(
        200,
        json={
            "html_attributions": [],
            "result": {
                "address_components": [],
                "business_status": "OPERATIONAL",
                "current_opening_hours": {},
                "delivery": True,
                "dine_in": True,
                "editorial_summary": {
                    "language": "en",
                    "overview": "Modern outpost of a longtime counter-serve pizza joint prepping New York-style slices & pies.",
                },
                "formatted_address": "1435 Broadway, New York, NY 10018, USA",
                "formatted_phone_number": "(646) 559-4878",
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
                "international_phone_number": "+1 646-559-4878",
                "name": "Joe's Pizza Broadway",
                "opening_hours": {},
                "photos": [],
                "place_id": "ChIJifIePKtZwokRVZ-UdRGkZzs",
                "plus_code": {},
                "price_level": 1,
                "rating": 4.5,
                "reference": "ChIJifIePKtZwokRVZ-UdRGkZzs",
                "reservable": False,
                "reviews": [],
                "secondary_opening_hours": [],
                "serves_breakfast": False,
                "serves_brunch": False,
                "serves_dinner": True,
                "serves_lunch": True,
                "takeout": True,
                "types": [
                    "meal_delivery",
                    "restaurant",
                    "food",
                    "point_of_interest",
                    "establishment",
                ],
                "url": "https://maps.google.com/?cid=4280570365733019477",
                "user_ratings_total": 13623,
                "utc_offset": -300,
                "vicinity": "1435 Broadway, New York",
                "website": "http://joespizzanyc.com/",
                "wheelchair_accessible_entrance": True,
            },
            "status": "OK",
        },
    ),
)
def test_add_review(client: TestClient):
    """Test case for add_review

    Add a new review about a restaurant
    """

    DbReview.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    DbRestaurant.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")

    create_review: Dict = {
        "photoUrl": "www.photouploaded.com",
        "starred": True,
        "favoriteFood": "pizza",
        "rating": 5,
        "restaurantId": "ChIJifIePKtZwokRVZ-UdRGkZzs",
        "content": "Awesome",
        "username": "theUser",
    }

    test_user: DbUser = DbUser(create_review["username"])
    test_user.update(
        actions=[
            DbUser.first_name.set("John"),
            DbUser.last_name.set("James"),
            DbUser.email.set("john@email.com"),
            DbUser.password.set("12345"),
            DbUser.id.set("1"),
        ]
    )
    test_user.save()
    assert DbUser.get(create_review["username"]).username == create_review["username"]

    headers: Dict = {}
    response: Response = client.request(
        "POST",
        "reviews",
        headers=headers,
        json=create_review,
    )

    review_id: str = response.json()["id"]
    review_record: DbReview = DbReview.get(review_id)

    assert response.status_code == 200
    assert response.json() == {
        "id": review_id,
        "user": {
            "id": test_user.id,
            "username": test_user.username,
            "firstName": test_user.first_name,
            "lastName": test_user.last_name,
            "email": test_user.email,
            "password": test_user.password,
        },
        "restaurant": {
            "id": create_review["restaurantId"],
            "name": "Joe's Pizza Broadway",
            "latitude": 40.7546795,
            "longitude": -73.9870291,
            "address": "1435 Broadway, New York, NY 10018, USA",
        },
        "rating": create_review["rating"],
        "content": create_review["content"],
        "photoUrl": create_review["photoUrl"],
        "favoriteFood": create_review["favoriteFood"],
        "starred": create_review["starred"],
        "createdAt": review_record.created_at,
        "updatedAt": review_record.updated_at,
    }


def test_delete_image(client: TestClient):
    """Test case for delete_image

    deletes an image
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/reviews/{reviewId}/image".format(reviewId="review_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


@mock_dynamodb
def test_delete_review(client: TestClient):
    """Test case for delete_review

    Deletes a review
    """

    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    (test_user, test_restaurant, test_review) = initTestItems()

    headers: Dict = {}
    response: Response = client.request(
        "DELETE",
        "reviews/{reviewId}".format(reviewId=test_review.id),
        headers=headers,
    )
    assert response.status_code == 204

    # trying to delete already deleted record
    response = client.request(
        "DELETE",
        "reviews/{reviewId}".format(reviewId=test_review.id),
        headers=headers,
    )
    assert response.status_code == 404


@mock_dynamodb
def test_get_review_by_id(client: TestClient):
    """Test case for get_review_by_id

    Find review by ID
    """

    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    (test_user, test_restaurant, test_review) = initTestItems()

    headers: Dict = {}
    response: Response = client.request(
        "GET",
        "reviews/{reviewId}".format(reviewId=test_review.id),
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_review.id,
        "user": {
            "id": test_user.id,
            "username": test_user.username,
            "firstName": test_user.first_name,
            "lastName": test_user.last_name,
            "email": test_user.email,
            "password": test_user.password,
        },
        "restaurant": {
            "id": test_restaurant.id,
            "name": test_restaurant.name,
            "latitude": test_restaurant.latitude,
            "longitude": test_restaurant.longitude,
            "address": test_restaurant.address,
        },
        "rating": test_review.rating,
        "content": test_review.content,
        "photoUrl": test_review.photo_url,
        "favoriteFood": test_review.favorite_food,
        "starred": test_review.starred,
        "createdAt": test_review.created_at,
        "updatedAt": test_review.updated_at,
    }

    # searching for review that doesn't exist
    response = client.request(
        "GET",
        "reviews/{reviewId}".format(reviewId="404"),
        headers=headers,
    )
    assert response.status_code == 404


def test_update_reviewby_id(client: TestClient):
    """Test case for update_reviewby_id

    Update an existing review
    """
    update_review = {
        "photo_url": "www.photouploaded.com",
        "starred": 1,
        "favorite_food": "pizza",
        "rating": 5,
        "content": "Awesome",
    }

    headers = {}
    response = client.request(
        "PUT",
        "/reviews/{reviewId}".format(reviewId="review_id_example"),
        headers=headers,
        json=update_review,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_upload_image(client: TestClient):
    """Test case for upload_image

    uploads an image
    """
    body = "/path/to/file"
    params = [("additional_metadata", "additional_metadata_example")]
    headers = {}
    response = client.request(
        "POST",
        "/reviews/{reviewId}/image".format(reviewId="review_id_example"),
        headers=headers,
        json=body,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
