from uuid import UUID
from typing import List

from app.core.excepcions import AppException
from fastapi import status
from redis import Redis

from app.repositories.product_repository import ProductRepository
from app.schemas.model import ProductResponse, CreateProduct, UpdateProduct
from app.utils.cache import (
    get_from_cache,
    set_to_cache,
    delete_from_cache,
    invalidate_pattern,
    build_cache_key,
)

#Product 5 mn
_PRODUCT_TTL = 300
#Paginated list 1min
_LIST_TTL = 60


def _get_product_or_404(repo: ProductRepository, product_id: UUID):
    product = repo.get_by_id(product_id)
    if product is None:
        raise AppException(
            message=f"Product {product_id} not found",
            error_code="PRODUCT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return product


def get_product(product_id: UUID, repo: ProductRepository, redis: Redis) -> ProductResponse:
    cache_key = build_cache_key("product", str(product_id))

    # Check cache first
    cached = get_from_cache(redis, cache_key)
    if cached is not None:
        return ProductResponse(**cached)

    #  Cache miss, hit the DB
    product = _get_product_or_404(repo, product_id)

    #Store in cache for next time
    response = ProductResponse.model_validate(product)
    set_to_cache(redis, cache_key, response.model_dump(mode="json"), _PRODUCT_TTL)
    return response


def list_products(skip: int, limit: int, repo: ProductRepository, redis: Redis) -> List[ProductResponse]:
    cache_key = build_cache_key("products", skip=skip, limit=limit)

    cached = get_from_cache(redis, cache_key)
    if cached is not None:
        return [ProductResponse(**p) for p in cached]

    products = repo.list(skip, limit)
    response = [ProductResponse.model_validate(p) for p in products]
    set_to_cache(redis, cache_key, [p.model_dump(mode="json") for p in response], _LIST_TTL)
    return response


def create_product(data: CreateProduct, repo: ProductRepository, redis: Redis) -> ProductResponse:
    product = repo.create(data)

    # All paginated list caches are now stale
    invalidate_pattern(redis, "products:*")
    return ProductResponse.model_validate(product)


def update_product(
    product_id: UUID, data: UpdateProduct, repo: ProductRepository, redis: Redis
) -> ProductResponse:
    product = _get_product_or_404(repo, product_id)
    product = repo.update(product, data)

    # Invalidate this product's cache entry, all list caches
    delete_from_cache(redis, build_cache_key("product", str(product_id)))
    invalidate_pattern(redis, "products:*")
    return ProductResponse.model_validate(product)


def delete_product(product_id: UUID, repo: ProductRepository, redis: Redis) -> None:
    product = _get_product_or_404(repo, product_id)
    repo.delete(product)

    delete_from_cache(redis, build_cache_key("product", str(product_id)))
    invalidate_pattern(redis, "products:*")
