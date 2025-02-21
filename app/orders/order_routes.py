from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from . import order_crud
from ..user.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return order_crud.create_order(db, order, current_user)


@router.get("/", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    return order_crud.get_orders(db, current_user)


@router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_orders(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(get_current_user)):
    return order_crud.update_orders(db, order_id, order, current_user)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return order_crud.get_order(db, order_id, current_user)


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return order_crud.delete_order(db, order_id, current_user)


