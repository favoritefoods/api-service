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

from pynamodb.expressions.update import Action

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
                result: Dict = response.json()["result"]

            restaurant = DbRestaurant(
                result["place_id"],
                name=result["name"],
                latitude=result["geometry"]["location"]["lat"],
                longitude=result["geometry"]["location"]["lng"],
                address=result["formatted_address"],
            )
            restaurant.save()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_review: DbReview = DbReview(
        uuid4().hex,
        created_at=str(datetime.utcnow()),
        username=create_review.username,
        restaurant_id=create_review.restaurant_id,
        rating=create_review.rating,
        favorite_food=create_review.favorite_food,
        starred=create_review.starred,
    )
    new_review.updated_at = new_review.created_at
    # optional request body properties
    if create_review.content:
        new_review.content = create_review.content
    if create_review.photo_url:
        new_review.photo_url = create_review.photo_url
    try:
        new_review.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Review(
        id=new_review.id,
        user=User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
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
        photo_url=new_review.photo_url,
        favorite_food=new_review.favorite_food,
        starred=new_review.starred,
        created_at=new_review.created_at,
        updated_at=new_review.updated_at,
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
) -> Response:
    """delete a review"""
    try:
        DbReview.get(reviewId).delete()
        return Response(status_code=204)
    except DbReview.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        # review info
        review: DbReview = DbReview.get(reviewId)

        # user info
        try:
            user: DbUser = DbUser.get(review.username)
        except DbUser.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # restaurant info
        try:
            restaurant: DbRestaurant = DbRestaurant.get(review.restaurant_id)
        except DbRestaurant.DoesNotExist:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return Review(
            id=review.id,
            user=User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
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
            rating=review.rating,
            content=review.content,
            photo_url=review.photo_url,
            favorite_food=review.favorite_food,
            starred=review.starred,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
    except DbReview.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        # review info
        review: DbReview = DbReview.get(reviewId)

        if update_review.rating:
            review.rating = update_review.rating
        if update_review.content:
            review.content = update_review.content
        if update_review.photo_url:
            review.photo_url = update_review.photo_url
        if update_review.favorite_food:
            review.favorite_food = update_review.favorite_food
        if update_review.starred is not None:
            review.starred = update_review.starred
        review.updated_at = str(datetime.utcnow())
        try:
            review.save()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # user info
        try:
            user: DbUser = DbUser.get(review.username)
        except DbUser.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # restaurant info
        try:
            restaurant: DbRestaurant = DbRestaurant.get(review.restaurant_id)
        except DbRestaurant.DoesNotExist:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return Review(
            id=review.id,
            user=User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
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
            rating=review.rating,
            content=review.content,
            photo_url=review.photo_url,
            favorite_food=review.favorite_food,
            starred=review.starred,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
    except DbReview.DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
