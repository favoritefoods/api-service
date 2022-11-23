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
from openapi_server.models.api_response import ApiResponse
from openapi_server.models.create_review import CreateReview
from openapi_server.models.review import Review
from openapi_server.models.update_review import UpdateReview


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
    create_review: CreateReview = Body(None, description="Create a new review about a restaurant"),
) -> Review:
    """Add a new review about a restaurant"""
    ...


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
    reviewId: int = Path(None, description="ID of review to update"),
    additional_metadata: str = Query(None, description="Additional Metadata"),
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
    reviewId: int = Path(None, description="Review id to delete"),
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
    reviewId: int = Path(None, description="ID of review to return"),
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
    reviewId: int = Path(None, description="ID of review to return"),
    update_review: UpdateReview = Body(None, description="Update an existent review on a restaurant"),
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
    reviewId: int = Path(None, description="ID of review to update"),
    additional_metadata: str = Query(None, description="Additional Metadata"),
    body: str = Body(None, description=""),
) -> ApiResponse:
    """"""
    ...
