# coding: utf-8

import os

from typing import Dict, List, Union  # noqa: F401
from dotenv import load_dotenv

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

from httpx import AsyncClient

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.list_restaurants import ListRestaurants
from openapi_server.models.list_reviews import ListReviews
from openapi_server.models.restaurant import Restaurant

load_dotenv()

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
) -> Union[ListRestaurants, Response]:
    """Returns all restauarants in given location radius"""
    results: List
    try:
        async with AsyncClient(base_url="https://maps.googleapis.com") as ac:
            response = await ac.get(
                f"/maps/api/place/nearbysearch/json?location={latitude}%2C{longitude}&radius={radius}&type=restaurant&key={os.environ.get('GOOGLE_API_KEY')}"
            )
            results = response.json()["results"]
    except:
        return Response(status_code=500)

    restaurants: List[Restaurant] = []
    for place in results:
        if place["business_status"] == "OPERATIONAL":
            restaurant: Restaurant = Restaurant(
                id=place["place_id"],
                name=place["name"],
                latitude=place["geometry"]["location"]["lat"],
                longitude=place["geometry"]["location"]["lng"],
                address=place["vicinity"],
            )
            restaurants.append(restaurant)

    return ListRestaurants(restaurants=restaurants)


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
    restaurantId: str = Path(
        None,
        description="ID of restaurant to return all reviews for a single restaurant",
    ),
) -> ListReviews:
    """Returns all reviews for a single restaurant"""
    ...
