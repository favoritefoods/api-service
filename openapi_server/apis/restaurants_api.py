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
from openapi_server.models.list_restaurants import ListRestaurants
from openapi_server.models.list_reviews import ListReviews


router = APIRouter()


@router.get(
    "/restaurants",
    responses={
        200: {"model": ListRestaurants, "description": "successful operation"},
        400: {"description": "Invalid query supplied"},
    },
    tags=["restaurants"],
    summary="Find restaurants in user location given",
    response_model_by_alias=True,
)
async def get_restaurants(
    longitude: float = Query(None, description="longitude of center"),
    latitude: float = Query(None, description="latitude of center"),
    radius: int = Query(None, description="radius"),
) -> ListRestaurants:
    """Returns all restauarants in given location radius"""
    ...


@router.get(
    "/restaurants/{restaurantId}/reviews",
    responses={
        200: {"model": ListReviews, "description": "Successful operation"},
        400: {"description": "Invalid ID supplied"},
    },
    tags=["restaurants"],
    summary="Find reviews by restaurant",
    response_model_by_alias=True,
)
async def get_review_by_restaurant(
    restaurantId: int = Path(None, description="ID of restaurant to return all reviews for a single restaurant"),
) -> ListReviews:
    """Returns all reviews for a single restaurant"""
    ...
