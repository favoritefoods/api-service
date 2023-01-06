# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.api_response import ApiResponse  # noqa: F401
from openapi_server.models.create_review import CreateReview  # noqa: F401
from openapi_server.models.review import Review  # noqa: F401
from openapi_server.models.update_review import UpdateReview  # noqa: F401


def test_add_review(client: TestClient):
    """Test case for add_review

    Add a new review about a restaurant
    """
    create_review = {
        "photo_url": "www.photouploaded.com",
        "starred": 1,
        "favorite_food": "pizza",
        "rating": 5,
        "restaurant_id": "19877",
        "user_id": "198772",
        "content": "Awesome",
    }

    headers = {}
    response = client.request(
        "POST",
        "/reviews",
        headers=headers,
        json=create_review,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_delete_image(client: TestClient):
    """Test case for delete_image

    deletes an image
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/reviews/{reviewId}/image".format(reviewId=56),
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
        "/reviews/{reviewId}".format(reviewId=56),
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
        "/reviews/{reviewId}".format(reviewId=56),
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
        "/reviews/{reviewId}".format(reviewId=56),
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
        "/reviews/{reviewId}/image".format(reviewId=56),
        headers=headers,
        json=body,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
