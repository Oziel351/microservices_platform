from uuid import UUID
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db_session
from app.schemas.model import Product, CreateProduct, UpdateProduct


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list(self, skip: int, limit: int) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create(self, data: CreateProduct) -> Product:
        product = Product(name=data.name, price=data.price, stock=data.stock)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: UpdateProduct) -> Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()


def get_product_repository(db: Session = Depends(get_db_session)) -> ProductRepository:
    return ProductRepository(db)
