from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.redis import redis_client
from app.repositories.product_repository import ProductRepository, get_product_repository
from app.schemas.model import CreateProduct, UpdateProduct, ProductResponse
from app.constants.api_response import ApiResponse
from app.services import product_service

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get("/", response_model=ApiResponse[list[ProductResponse]])
def get_products(skip: int = 0, limit: int = 10, repo: ProductRepository = Depends(get_product_repository)):
    products = product_service.list_products(skip, limit, repo, redis_client)
    return ApiResponse(message="Products retrieved successfully", data=products)


@products_router.get("/{product_id}", response_model=ApiResponse[ProductResponse])
def get_product(product_id: UUID, repo: ProductRepository = Depends(get_product_repository)):
    product = product_service.get_product(product_id, repo, redis_client)
    return ApiResponse(message="Product retrieved successfully", data=product)


@products_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[ProductResponse])
def create_product(data: CreateProduct, repo: ProductRepository = Depends(get_product_repository)):
    product = product_service.create_product(data, repo, redis_client)
    return ApiResponse(message=f"Product '{product.name}' created successfully", data=product)


@products_router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[ProductResponse])
def update_product(product_id: UUID, data: UpdateProduct, repo: ProductRepository = Depends(get_product_repository)):
    product = product_service.update_product(product_id, data, repo, redis_client)
    return ApiResponse(message="Product updated successfully", data=product)


@products_router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: UUID, repo: ProductRepository = Depends(get_product_repository)):
    product_service.delete_product(product_id, repo, redis_client)
    return ApiResponse(message=f"Product {product_id} deleted successfully")
