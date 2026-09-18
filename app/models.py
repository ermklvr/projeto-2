from sqlalchemy import String, Numeric, ForeignKey, Enum

from sqlalchemy.orm import Mapped, relationship, mapped_column

from .database import Base
from decimal import Decimal

import enum

from datetime import datetime
from sqlalchemy import DateTime

class MovementType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Product(Base):
    __tablename__ = "produtos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name:  Mapped[str] = mapped_column(String(100), nullable=False)
    
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
    
    category_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    
    active: Mapped[bool] = mapped_column(default=True, nullable=False) #para soft delete
    
    #relações
    category: Mapped["Category"] = relationship(back_populates="products")
    movements: Mapped[list["Movement"]] = relationship(back_populates="product")
    
    
class Category(Base):
    __tablename__ = "categorias"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name:  Mapped[str] = mapped_column(String(50), nullable=False)
    
    products: Mapped[list["Product"]] = relationship(back_populates="category")
    

class Movement(Base):
    __tablename__ = "movimentacoes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    product_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    
    type: Mapped[MovementType] = mapped_column(Enum(MovementType), nullable=False)
    
    quantity: Mapped[int] = mapped_column(nullable=False)
    
    date: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow,
    nullable=False
)
    product: Mapped["Product"] = relationship(back_populates="movements")
        

