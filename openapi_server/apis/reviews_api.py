# coding: utf-8

import os
from typing import Dict, List  # noqa: F401
from datetime import datetime
from uuid import uuid4
from httpx import AsyncClient

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
from openapi_server.models.api_response import ApiResponse
from openapi_server.models.create_review import CreateReview
from openapi_server.models.review import Review
from openapi_server.models.update_review import UpdateReview
from openapi_server.models.user import User
from openapi_server.models.restaurant import Restaurant
from openapi_server.orms.review import DbReview
from openapi_server.orms.user import DbUser
from openapi_server.orms.restaurant import DbRestaurant


router = APIRouter()


@router.post(
    "/reviews",
    responses={
        200: {"model": Review, "description": "Successful operation"},
        405: {"description": "Invalid input"},
    },
    tags=["reviews"],
    summary="Add a new review about a restaurant",
    response_model_by_alias=True,
)
async def add_review(
    create_review: CreateReview = Body(
        None, description="Create a new review about a restaurant"
    ),
) -> Review:
    """Add a new review about a restaurant"""
    try:
        user: DbUser = DbUser.get(create_review.username)
    except DbUser.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # check if the restaurant information is stored in the database; create the item if not
    try:
        restaurant: DbRestaurant = DbRestaurant.get(create_review.restaurant_id)
    except DbRestaurant.DoesNotExist:
        try:
            async with AsyncClient(base_url="https://maps.googleapis.com") as ac:
                response = await ac.get(
                    f"/maps/api/place/details/json?place_id={create_review.restaurant_id}&key={os.environ.get('GOOGLE_API_KEY')}"
                )
                result = response.json()["result"]

            restaurant = DbRestaurant(result["place_id"])
            restaurant.update(
                actions=[
                    DbRestaurant.name.set(result["name"]),
                    DbRestaurant.latitude.set(result["geometry"]["location"]["lat"]),
                    DbRestaurant.longitude.set(result["geometry"]["location"]["lng"]),
                    DbRestaurant.address.set(result["formatted_address"]),
                ]
            )
            restaurant.save()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_review: DbReview = DbReview(uuid4().hex)
    new_review.update(
        actions=[
            DbReview.created_at.set(str(datetime.utcnow())),
            DbReview.username.set(create_review.username),
            DbReview.restaurantId.set(create_review.restaurant_id),
            DbReview.rating.set(create_review.rating),
            DbReview.favorite_food.set(create_review.favorite_food),
            DbReview.starred.set(create_review.starred),
        ]
    )
    actions = [DbReview.updated_at.set(new_review.created_at)]
    # optional request body properties
    if create_review.content:
        actions.append(DbReview.content.set(create_review.content))
    if create_review.photo_url:
        actions.append(DbReview.photo_url.set(create_review.photo_url))

    new_review.update(actions)
    try:
        new_review.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Review(
        id=new_review.id,
        user=User(
            id=user.id,
            username=user.username,
            firstName=user.first_name,
            lastName=user.last_name,
            email=user.email,
            password=user.password,
        ),
        restaurant=Restaurant(
            id=restaurant.id,
            name=restaurant.name,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            address=restaurant.address,
        ),
        rating=new_review.rating,
        content=new_review.content,
        photoUrl=new_review.photo_url,
        favoriteFood=new_review.favorite_food,
        starred=new_review.starred,
        createdAt=new_review.created_at,
        updatedAt=new_review.updated_at,
    )


@router.delete(
    "/reviews/{reviewId}/image",
    responses={
        204: {"description": "Successful operation"},
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Review or image not found"},
    },
    tags=["reviews"],
    summary="deletes an image",
    response_model_by_alias=True,
)
async def delete_image(
    reviewId: str = Path(None, description="ID of review to update"),
) -> None:
    """"""
    ...


@router.delete(
    "/reviews/{reviewId}",
    responses={
        204: {"description": "Successful operation"},
        400: {"description": "Invalid review value"},
    },
    tags=["reviews"],
    summary="Deletes a review",
    response_model_by_alias=True,
)
async def delete_review(
    reviewId: str = Path(None, description="Review id to delete"),
) -> None:
    """delete a review"""
    ...


@router.get(
    "/reviews/{reviewId}",
    responses={
        200: {"model": Review, "description": "successful operation"},
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Review not found"},
    },
    tags=["reviews"],
    summary="Find review by ID",
    response_model_by_alias=True,
)
async def get_review_by_id(
    reviewId: str = Path(None, description="ID of review to return"),
) -> Review:
    """Returns a single review"""
    ...


@router.put(
    "/reviews/{reviewId}",
    responses={
        200: {"model": Review, "description": "Successful operation"},
        400: {"description": "Invalid ID supplied"},
        404: {"description": "Review not found"},
        405: {"description": "Validation exception"},
    },
    tags=["reviews"],
    summary="Update an existing review",
    response_model_by_alias=True,
)
async def update_reviewby_id(
    reviewId: str = Path(None, description="ID of review to return"),
    update_review: UpdateReview = Body(
        None, description="Update an existent review on a restaurant"
    ),
) -> Review:
    """Update an existing review by Id"""
    ...


@router.post(
    "/reviews/{reviewId}/image",
    responses={
        200: {"model": ApiResponse, "description": "successful operation"},
    },
    tags=["reviews"],
    summary="uploads an image",
    response_model_by_alias=True,
)
async def upload_image(
    reviewId: str = Path(None, description="ID of review to update"),
    additional_metadata: str = Query(None, description="Additional Metadata"),
    body: str = Body(None, description=""),
) -> ApiResponse:
    """"""
    ...
