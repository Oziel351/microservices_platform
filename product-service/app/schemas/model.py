from sqlalchemy import Integer, String, DateTime, func, UUID, Numeric, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID as UUID_type
from decimal import Decimal



# Declarative base 
class Base(DeclarativeBase):
    pass


#Define the structure for de products table using mapped_colum 

class Product(Base):
    __tablename__ = "products"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    price:Mapped[int] = mapped_column(Numeric(10, 2), nullable=False)
    stock:Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Constrains for table data
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
        CheckConstraint('stock >= 0', name='check_stock_positive'),
    )

    #Debbuging method for developers
    def __repr__(self):
        return (f"Product(id={self.id}, name={self.name!r}, "
                f"price={self.price}, stock={self.stock})")
    
    #For typcal users 
    def __str__(self):
        return f"{self.name} - ${self.price} (Stock: {self.stock})"


# Pydantic response model (DTO) for FastAPI
class ProductResponse(BaseModel):
    id: UUID_type
    name: str
    price: Decimal
    stock: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class CreateProduct(BaseModel):
    name: str
    price: Decimal
    stock: int = 0

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
