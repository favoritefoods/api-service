# coding: utf-8

import uuid

from typing import Dict, List, Union, Optional  # noqa: F401

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
    HTTPException,
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
from openapi_server.models.favorite_food import FavoriteFood
from openapi_server.orms.user import DbUser, DbFavoriteFood


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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_user: DbUser = DbUser(
        create_user.username,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        # should let Cognito handle pw storage and access in prod
        password=create_user.password,
        id=uuid.uuid4().hex,  # can use Cognito id in prod
    )
    try:
        new_user.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return User(
        id=new_user.id,
        username=new_user.username,
        firstName=new_user.first_name,
        lastName=new_user.last_name,
        email=new_user.email,
        password=new_user.password,
    )


@router.delete(
    "/users/{username}/friends",
    responses={
        200: {"model": ListFriends, "description": "successful operation"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Remove all connections to friends of a user",
    response_model_by_alias=True,
)
async def delete_friends(
    username: str = Path(None, description="Name of user"),
) -> ListFriends:
    """Unlink the connection of a user&#39;s friends list from their FB friends list, and remove all friends from a user&#39;s friends list since they are 1-to-1"""
    ...


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
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        user: DbUser = DbUser.get(username)
    except DbUser.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    favorite_foods: List[FavoriteFood] = []
    for item in user.favorite_foods:
        food: FavoriteFood = FavoriteFood(id=item.id, name=item.name)
        favorite_foods.append(food)
    return ListFavoriteFoods(favoriteFoods=favorite_foods)


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
    """Returns all friends of a single user"""
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
) -> User:
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
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        user: DbUser = DbUser.get(username)
    except DbUser.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    fav_foods: List[DbFavoriteFood] = []  # to be saved in the database
    favorite_foods: List[FavoriteFood] = []  # to be returned in the response
    for item in list_favorite_foods.favorite_foods:
        db_food: DbFavoriteFood = DbFavoriteFood(id=item.id, name=item.name)
        fav_foods.append(db_food)
        food: FavoriteFood = FavoriteFood(id=item.id, name=item.name)
        favorite_foods.append(food)
    user.favorite_foods = fav_foods
    try:
        user.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ListFavoriteFoods(favoriteFoods=favorite_foods)


@router.put(
    "/users/{username}/friends",
    responses={
        200: {"model": ListFriends, "description": "successful operation"},
        404: {"description": "User not found"},
    },
    tags=["users"],
    summary="Update friends of a user",
    response_model_by_alias=True,
)
async def update_friends(
    username: str = Path(None, description="Name of user"),
) -> ListFriends:
    """Refresh or initialize a user&#39;s friends list to match 1-to-1 to their Facebook friends that have accounts, and return the list"""
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
) -> Optional[Response]:
    """This can only be done by the logged in user."""
    try:
        user: DbUser = DbUser.get(username)
    except DbUser.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    old_user_item: Union[DbUser, None]
    if update_user.username and update_user.username != user.username:
        try:
            DbUser.get(update_user.username)
            return Response(status_code=409)
        except DbUser.DoesNotExist:
            old_user_item = DbUser.get(user.username)
            user.username = update_user.username
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        old_user_item = None
    if update_user.first_name:
        user.first_name = update_user.first_name
    if update_user.last_name:
        user.last_name = update_user.last_name
    if update_user.email:
        user.email = update_user.email
    if update_user.password:
        user.password = update_user.password
    try:
        user.save()
        if old_user_item:
            old_user_item.delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return None
