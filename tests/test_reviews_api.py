# coding: utf-8

import httpx
from typing import Dict

from fastapi.testclient import TestClient

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


@mock_dynamodb
def test_add_review(client: TestClient):
    """Test case for add_review

    Add a new review about a restaurant
    """

    DbReview.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    DbRestaurant.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")

    create_review = {
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

    headers = {}
    response = client.request(
        "POST",
        "reviews",
        headers=headers,
        json=create_review,
    )

    review_id = response.json()["id"]
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


def test_delete_review(client: TestClient):
    """Test case for delete_review

    Deletes a review
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/reviews/{reviewId}".format(reviewId="review_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_review_by_id(client: TestClient):
    """Test case for get_review_by_id

    Find review by ID
    """

    headers = {}
    response = client.request(
        "GET",
        "/reviews/{reviewId}".format(reviewId="review_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


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
