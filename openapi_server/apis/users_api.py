# coding: utf-8

import uuid

from typing import Dict, List, Union  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.create_user import CreateUser
from openapi_server.models.list_favorite_foods import ListFavoriteFoods
from openapi_server.models.list_friends import ListFriends
from openapi_server.models.list_reviews import ListReviews
from openapi_server.models.login_payload import LoginPayload
from openapi_server.models.login_user import LoginUser
from openapi_server.models.update_user import UpdateUser
from openapi_server.models.user import User
from openapi_server.orms.user import DbUser


router = APIRouter()


@router.post(
    "/users",
    responses={
        200: {"model": User, "description": "successful operation"},
        409: {"description": "Username already exists"},
    },
    tags=["users"],
    summary="Create user",
    response_model_by_alias=True,
)
async def create_user(
    create_user: CreateUser = Body(None, description="Created user object"),
) -> Union[User, Response]:
    """"""
    try:
        DbUser.get(create_user.username)
        return Response(status_code=409)
    except DbUser.DoesNotExist:
        pass
    except:
        return Response(status_code=500)

    new_user: DbUser = DbUser(create_user.username)
    new_user.update(
        actions=[
            DbUser.first_name.set(create_user.first_name),
            DbUser.last_name.set(create_user.last_name),
            DbUser.email.set(create_user.email),
            # should let Cognito handle pw storage and access in prod
            DbUser.password.set(create_user.password),
            DbUser.id.set(uuid.uuid4().hex),  # can use Cognito id in prod
        ]
    )
    try:
        new_user.save()
    except:
        return Response(status_code=500)

    return User(
        id=new_user.id,
        username=new_user.username,
        firstName=new_user.first_name,
        lastName=new_user.last_name,
        email=new_user.email,
        password=new_user.password,
    )


@router.delete(
    "/users/{username}",
    responses={
        204: {"description": "Successful operation"},
        # not sure if this code '400' is necessary (front-end check?)
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Delete user",
    response_model_by_alias=True,
)
async def delete_user(
    username: str = Path(None, description="Name of user that needs to be deleted"),
) -> Response:
    """This can only be done by the logged in user."""
    try:
        DbUser.get(username).delete()
        return Response(status_code=204)
    except DbUser.DoesNotExist:
        return Response(status_code=404)
    except:
        return Response(status_code=500)


@router.get(
    "/users/{username}/favorite-foods",
    responses={
        200: {"model": ListFavoriteFoods, "description": "successful operation"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Get favorite foods of a user",
    response_model_by_alias=True,
)
async def get_favorite_foods(
    username: str = Path(None, description="Name of user"),
) -> ListFavoriteFoods:
    """"""
    ...


@router.get(
    "/users/{username}/friends",
    responses={
        200: {"model": ListFriends, "description": "successful operation"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Get friends of a user",
    response_model_by_alias=True,
)
async def get_friends(
    username: str = Path(None, description="Name of user"),
) -> ListFriends:
    """"""
    ...


@router.get(
    "/users/{username}/reviews",
    responses={
        200: {"model": ListReviews, "description": "successful operation"},
        400: {"description": "Invalid username supplied"},
    },
    tags=["users"],
    summary="Get reviews by user name",
    response_model_by_alias=True,
)
async def get_reviews_by_username(
    username: str = Path(
        None, description="The name of user to return user&#39;s reviews"
    ),
) -> ListReviews:
    """Returns all reviews by a single user"""
    ...


@router.get(
    "/users/{username}",
    responses={
        200: {"model": User, "description": "successful operation"},
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Get user by user name",
    response_model_by_alias=True,
)
async def get_user_by_name(
    username: str = Path(None, description="The name that needs to be fetched"),
) -> Union[User, Response]:
    """"""
    try:
        user: DbUser = DbUser.get(username)
        return User(
            id=user.id,
            username=user.username,
            firstName=user.first_name,
            lastName=user.last_name,
            email=user.email,
            password=user.password,
        )
    except DbUser.DoesNotExist:
        return Response(status_code=404)
    except:
        return Response(status_code=500)


@router.post(
    "/users/login",
    responses={
        200: {"model": LoginPayload, "description": "successful operation"},
        400: {"description": "Invalid username/password supplied"},
    },
    tags=["users"],
    summary="Logs user into the system",
    response_model_by_alias=True,
)
async def login_user(
    login_user: LoginUser = Body(None, description="Login information"),
) -> LoginPayload:
    """"""
    ...


@router.post(
    "/users/logout",
    responses={
        204: {"description": "successful operation"},
    },
    tags=["users"],
    summary="Logs out current logged in user session",
    response_model_by_alias=True,
)
async def logout_user() -> None:
    """"""
    ...


@router.put(
    "/users/{username}/favorite-foods",
    responses={
        200: {"model": ListFavoriteFoods, "description": "successful operation"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Update favorite foods of a user",
    response_model_by_alias=True,
)
async def update_favorite_foods(
    username: str = Path(None, description="Name of user"),
    list_favorite_foods: ListFavoriteFoods = Body(
        None, description="Update user&#39;s list of favorite foods"
    ),
) -> ListFavoriteFoods:
    """This can only be done by the logged in user."""
    ...


@router.put(
    "/users/{username}",
    responses={
        200: {"description": "successful operation"},
    },
    tags=["users"],
    summary="Update user",
    response_model_by_alias=True,
)
async def update_user(
    username: str = Path(None, description="Name of user that need to be updated"),
    update_user: UpdateUser = Body(
        None, description="Update an existent user in the store"
    ),
) -> None:
    """This can only be done by the logged in user."""
    ...
