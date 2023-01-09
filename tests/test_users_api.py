# coding: utf-8

import httpx
from typing import Dict, List, Union, Tuple

from fastapi.testclient import TestClient

from moto import mock_dynamodb

from openapi_server.models.create_user import CreateUser  # noqa: F401
from openapi_server.models.list_favorite_foods import ListFavoriteFoods  # noqa: F401
from openapi_server.models.list_friends import ListFriends  # noqa: F401
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

    create_user: Dict = {
        "firstName": "John",
        "lastName": "James",
        "password": "12345",
        "email": "john@email.com",
        "username": "theUser",
    }

    headers: Dict = {}
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
    }

    # create user with same values
    response = client.request(
        "POST",
        "users",
        headers=headers,
        json=create_user,
    )
    assert response.status_code == 409


def test_delete_friends(client: TestClient):
    """Test case for delete_friends

    Remove all connections to friends of a user
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/users/{username}/friends".format(username="username_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


@mock_dynamodb
def test_delete_user(client: TestClient):
    """Test case for delete_user

    Delete user
    """

    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    test_create_user(client)  # using above test to create a user w/ username="theUser"

    headers: Dict = {}
    response: httpx.Response = client.request(
        "DELETE",
        "users/{username}".format(username="theUser"),
        headers=headers,
    )
    assert response.status_code == 204

    # trying to delete already deleted record
    response = client.request(
        "DELETE",
        "users/{username}".format(username="theUser"),
        headers=headers,
    )
    assert response.status_code == 404


@mock_dynamodb
def test_get_favorite_foods(client: TestClient):
    """Test case for get_favorite_foods

    Get favorite foods of a user
    """

    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    test_create_user(client)

    headers: Dict = {}
    response: httpx.Response = client.request(
        "GET",
        "users/{username}/favorite-foods".format(username="theUser"),
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "favoriteFoods": [],
    }

    response = client.request(
        "GET",
        "users/{username}/favorite-foods".format(username="notTheUser"),
        headers=headers,
    )
    assert response.status_code == 404


def test_get_friends(client: TestClient):
    """Test case for get_friends

    Get friends of a user
    """

    headers = {}
    response = client.request(
        "GET",
        "/users/{username}/friends".format(username="username_example"),
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


@mock_dynamodb
def test_get_user_by_name(client: TestClient):
    """Test case for get_user_by_name

    Get user by user name
    """
    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    test_create_user(client)  # using above test to create a user w/ username="theUser"

    headers: Dict = {}
    response: httpx.Response = client.request(
        "GET",
        "users/{username}".format(username="theUser"),
        headers=headers,
    )
    user_record: DbUser = DbUser.get("theUser")

    assert response.status_code == 200
    assert response.json() == {
        "id": user_record.id,
        "username": user_record.username,
        "firstName": user_record.first_name,
        "lastName": user_record.last_name,
        "email": user_record.email,
        "password": user_record.password,
    }

    # searching for username that doesn't exist
    response = client.request(
        "GET",
        "users/{username}".format(username="notTheUser"),
        headers=headers,
    )
    assert response.status_code == 404


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


@mock_dynamodb
def test_update_favorite_foods(client: TestClient):
    """Test case for update_favorite_foods

    Update favorite foods of a user
    """
    list_favorite_foods: Dict[str, List[Dict[str, Union[int, str]]]] = {
        "favoriteFoods": [
            {"id": 1, "name": "sushi"},
            {"id": 2, "name": "pizza"},
        ],
    }

    DbUser.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    client = TestClient(app, base_url="http://0.0.0.0:8080/api/v1/")
    test_create_user(client)

    headers: Dict = {}
    response: httpx.Response = client.request(
        "PUT",
        "users/{username}/favorite-foods".format(username="theUser"),
        headers=headers,
        json=list_favorite_foods,
    )
    assert response.status_code == 200
    assert response.json() == {
        "favoriteFoods": [
            {"id": 1, "name": "sushi"},
            {"id": 2, "name": "pizza"},
        ],
    }

    response = client.request(
        "PUT",
        "users/{username}/favorite-foods".format(username="notTheUser"),
        headers=headers,
        json=list_favorite_foods,
    )
    assert response.status_code == 404


def test_update_friends(client: TestClient):
    """Test case for update_friends

    Update friends of a user
    """

    headers = {}
    response = client.request(
        "PUT",
        "/users/{username}/friends".format(username="username_example"),
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
        "username": "theUser",
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
