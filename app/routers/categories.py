from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Category
from ..schemas import CategoryCreate, CategoryResponse



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
    new_category = Category(
        name = category.name
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

#READ
@router.get("/",  response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/{category_id}",  response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
    ):
    category = db.query(Category).filter(Category.id == category_id).first()
    
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
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(status_code = 404, detail="Category not found")
        
    db_category.name  = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


#DELETE
@router.delete("/{category_id}")

def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted sucessfully"}