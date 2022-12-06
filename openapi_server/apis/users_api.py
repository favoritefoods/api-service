# coding: utf-8

from typing import Dict, List  # noqa: F401

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
from openapi_server.models.list_reviews import ListReviews
from openapi_server.models.login_user import LoginUser
from openapi_server.models.update_user import UpdateUser
from openapi_server.models.user import User
from openapi_server.orms.user import DbUser


router = APIRouter()


@router.post(
    "/users",
    responses={
        200: {"model": User, "description": "successful operation"},
    },
    tags=["users"],
    summary="Create user",
    response_model_by_alias=True,
)
async def create_user(
    create_user: CreateUser = Body(None, description="Created user object"),
) -> User:
    """"""
    new_user: DbUser = DbUser(create_user.username)
    new_user.update(
        actions=[
            DbUser.first_name.set(create_user.first_name),
            DbUser.last_name.set(create_user.last_name),
            DbUser.email.set(create_user.email),
            DbUser.password.set(create_user.password),
        ]
    )
    new_user.save()


@router.delete(
    "/users/{username}",
    responses={
        204: {"description": "Successful operation"},
        400: {"description": "Invalid username supplied"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Delete user",
    response_model_by_alias=True,
)
async def delete_user(
    username: str = Path(None, description="Name of user that needs to be deleted"),
) -> None:
    """This can only be done by the logged in user."""
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
    username: str = Path(
        None, description="The name that needs to be fetched. Use user1 for testing. "
    ),
) -> User:
    """"""
    ...


@router.post(
    "/users/login",
    responses={
        200: {"model": str, "description": "successful operation"},
        400: {"description": "Invalid username/password supplied"},
    },
    tags=["users"],
    summary="Logs user into the system",
    response_model_by_alias=True,
)
async def login_user(
    login_user: LoginUser = Body(None, description="Login information"),
) -> str:
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
