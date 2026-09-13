from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category
from ..schemas import CategoryCreate, CategoryResponse
from ..exceptions import CategoryHasProductsError, CategoryNotFoundError
from .. import crud

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

#CRUD
#CREATE
@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
    ):
    try:
        return crud.create_category(db,category)
    except Exception:
        raise HTTPException(status_code=404, detail="Category not found")

#READ
@router.get("/",  response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)
    


@router.get("/{category_id}",  response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
    ):
    category = crud.get_category_by_id(db,category_id)
    
    if not category:
        raise HTTPException(status_code = 404, detail="Category not found")
    
    return category
#UPDATE
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category (
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.update_category(db,category_id,category)    
    except CategoryNotFoundError:
        raise HTTPException(status_code = 404, detail="Category not found")
   


#DELETE
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_category(db, category_id)
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    except CategoryHasProductsError:
        raise HTTPException(status_code=409, detail="Cannot delete category with linked products")
    return