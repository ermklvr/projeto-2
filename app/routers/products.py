from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product,Category
from ..schemas import ProductCreate, ProductResponse

from decimal import Decimal

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

#CRUD

#CREATE
@router.post("/", response_model=ProductResponse)
def new_product (
   product: ProductCreate,
   db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == product.category_id).first()
        
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    new_product= Product(
        name = product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id   
    )      
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product

#REMOVE


#UPDATE


#DELTE