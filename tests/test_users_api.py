# coding: utf-8

import typing
import httpx

from fastapi.testclient import TestClient

from moto import mock_dynamodb

from openapi_server.models.create_user import CreateUser  # noqa: F401
from openapi_server.models.list_reviews import ListReviews  # noqa: F401
from openapi_server.models.login_payload import LoginPayload  # noqa: F401
from openapi_server.models.login_user import LoginUser  # noqa: F401
from openapi_server.models.update_user import UpdateUser  # noqa: F401
from openapi_server.models.user import User  # noqa: F401
from openapi_server.main import app
from openapi_server.orms.user import DbUser


@mock_dynamodb
def test_create_user(client: TestClient):
    """Test case for create_user

    Create user
    """

    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")

    create_user: typing.Dict = {
        "firstName": "John",
        "lastName": "James",
        "password": "12345",
        "email": "john@email.com",
        "username": "theUser",
    }

    headers: typing.Dict = {}
    response: httpx.Response = client.request(
        "POST",
        "users",
        headers=headers,
        json=create_user,
    )
    user_record: DbUser = DbUser.get(create_user["username"])

    assert response.status_code == 200
    assert response.json() == {
        "id": user_record.id,
        "username": create_user["username"],
        "firstName": create_user["firstName"],
        "lastName": create_user["lastName"],
        "email": create_user["email"],
        "password": create_user["password"],
        "favoriteFoods": [],
        "friends": [],
    }


def test_delete_user(client: TestClient):
    """Test case for delete_user

    Delete user
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/users/{username}".format(username="username_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_reviews_by_username(client: TestClient):
    """Test case for get_reviews_by_username

    Get reviews by user name
    """

    headers = {}
    response = client.request(
        "GET",
        "/users/{username}/reviews".format(username="username_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_user_by_name(client: TestClient):
    """Test case for get_user_by_name

    Get user by user name
    """

    headers = {}
    response = client.request(
        "GET",
        "/users/{username}".format(username="username_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_login_user(client: TestClient):
    """Test case for login_user

    Logs user into the system
    """
    login_user = {"password": "12345", "email": "john@email.com"}

    headers = {}
    response = client.request(
        "POST",
        "/users/login",
        headers=headers,
        json=login_user,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_logout_user(client: TestClient):
    """Test case for logout_user

    Logs out current logged in user session
    """

    headers = {}
    response = client.request(
        "POST",
        "/users/logout",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_update_user(client: TestClient):
    """Test case for update_user

    Update user
    """
    update_user = {
        "first_name": "John",
        "last_name": "James",
        "password": "12345",
        "email": "john@email.com",
        "friends": [
            {
                "first_name": "John",
                "last_name": "James",
                "password": "12345",
                "id": 10,
                "email": "john@email.com",
                "friends": [None, None],
                "username": "theUser",
                "favorite_foods": [
                    {
                        "reviews": [
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                        ],
                        "name": "sushi",
                        "id": 10,
                    },
                    {
                        "reviews": [
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                        ],
                        "name": "sushi",
                        "id": 10,
                    },
                ],
            },
            {
                "first_name": "John",
                "last_name": "James",
                "password": "12345",
                "id": 10,
                "email": "john@email.com",
                "friends": [None, None],
                "username": "theUser",
                "favorite_foods": [
                    {
                        "reviews": [
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                        ],
                        "name": "sushi",
                        "id": 10,
                    },
                    {
                        "reviews": [
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                            {
                                "photo_url": "www.photouploaded.com",
                                "rating": 5,
                                "id": 10,
                                "restaurant_id": 19877,
                                "user_id": 198772,
                                "content": "Awesome",
                            },
                        ],
                        "name": "sushi",
                        "id": 10,
                    },
                ],
            },
        ],
        "username": "theUser",
        "favorite_foods": [
            {
                "reviews": [
                    {
                        "photo_url": "www.photouploaded.com",
                        "rating": 5,
                        "id": 10,
                        "restaurant_id": 19877,
                        "user_id": 198772,
                        "content": "Awesome",
                    },
                    {
                        "photo_url": "www.photouploaded.com",
                        "rating": 5,
                        "id": 10,
                        "restaurant_id": 19877,
                        "user_id": 198772,
                        "content": "Awesome",
                    },
                ],
                "name": "sushi",
                "id": 10,
            },
            {
                "reviews": [
                    {
                        "photo_url": "www.photouploaded.com",
                        "rating": 5,
                        "id": 10,
                        "restaurant_id": 19877,
                        "user_id": 198772,
                        "content": "Awesome",
                    },
                    {
                        "photo_url": "www.photouploaded.com",
                        "rating": 5,
                        "id": 10,
                        "restaurant_id": 19877,
                        "user_id": 198772,
                        "content": "Awesome",
                    },
                ],
                "name": "sushi",
                "id": 10,
            },
        ],
    }

    headers = {}
    response = client.request(
        "PUT",
        "/users/{username}".format(username="username_example"),
        headers=headers,
        json=update_user,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
