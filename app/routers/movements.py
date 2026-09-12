from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product,Category,Movement, MovementType
from ..schemas import MovementCreate, MovementResponse

from decimal import Decimal

from .. import crud

router = APIRouter(
    prefix="/movements",
    tags=["Movements"]
)


#CRUD

#CREATE

@router.post("/", response_model=MovementResponse)
def create_movement(
    movement:MovementCreate,
    db: Session = Depends(get_db)
):
    new_movement = crud.create_movement(db,movement)
    
    if not new_movement:
            raise HTTPException(status_code=404, detail="Product not found or insufficient stock")
        
    return new_movement
        