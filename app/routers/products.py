from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product,Category
from ..schemas import ProductCreate, ProductResponse

from decimal import Decimal

from .. import crud


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
    new_product = crud.new_product(db,product)
        
    if not new_product:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return new_product

#READ
@router.get("/" , response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@router.get("/{product_id}",  response_model=ProductResponse)
def get_product_by_id (
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product_by_id(db,product_id)
    
    if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

#UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product (
    product_id : int,
    product : ProductCreate,
    db: Session = Depends(get_db)
):
    updated_product = crud.update_product(db, product_id, product)
    
    if not updated_product:
        raise HTTPException(status_code = 404, detail="Product not found")
            
    return updated_product

#DELETE
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)                            
):
   deleted_product = crud.delete_product(db,product_id)
   
   if not deleted_product:
       raise HTTPException(status_code = 404, detail="Product not found")
   
   return {"message": "Product deleted successfully"}