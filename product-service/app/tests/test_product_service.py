from uuid import uuid4
from unittest.mock import MagicMock
from decimal import Decimal


import pytest


from app.services import product_service
from app.schemas.model import Product, CreateProduct
from app.core.excepcions import AppException


def make_product(**overrides):
    defaults = dict(id=uuid4(), name="Mouse", price=Decimal("10.00"), stock=5)
    defaults.update(overrides)
    return Product(**defaults)


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def redis():
    r = MagicMock()
    # Simulate cache for tests by default
    r.get.return_value = None
    return r

class TestGetProduct:
    def test_returns_product_from_db_on_cache_miss(self, repo, redis):
        product = make_product()
        repo.get_by_id.return_value = product

        result = product_service.get_product(product.id, repo, redis)

        assert result.id == product.id
        repo.get_by_id.assert_called_once_with(product.id)

    def test_raises_404_when_product_missing(self, repo, redis):
        repo.get_by_id.return_value = None

        with pytest.raises(AppException) as exc_info:
            product_service.get_product(uuid4(), repo, redis)

        assert exc_info.value.error_code == "PRODUCT_NOT_FOUND"

    def test_returns_cached_value_without_hitting_repo(self, repo, redis):
        cached_payload = {
            "id": str(uuid4()), "name": "Mouse",
            "price": "10.00", "stock": 5,
            "created_at": None, "updated_at": None,
        }
        redis.get.return_value = '{"id": "%s", "name": "Mouse", "price": "10.00", "stock": 5, "created_at": null, "updated_at": null}' % cached_payload["id"]

        product_service.get_product(uuid4(), repo, redis)

        repo.get_by_id.assert_not_called()