from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from .. import models, schemas
from ..user.auth import get_current_user
from sqlalchemy.orm import joinedload
import json


def create_order(
    db: Session, order: schemas.OrderCreate, current_user: schemas.UserResponse
):
    user_id = current_user.id

    print(order.product_ids)
    products = (
        db.query(models.Product).filter(models.Product.id.in_(order.product_ids)).all()
    )

    if len(products) != len(order.product_ids):
        raise HTTPException(
            status_code=400, detail="One or more products are not available"
        )

    db_order = models.Order(
        user_id=user_id, products=products
    )  # ✅ Add products directly
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "status": db_order.status,
        "products": [
            schemas.ProductResponse.model_validate(p) for p in db_order.products
        ],
    }

def get_orders(db: Session, current_user: schemas.UserResponse):
    user_id = current_user.id

    # Fetch orders along with related products
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .options(joinedload(models.Order.products))  # Eagerly load products
        .all()
    )

    # Convert to response model
    order_responses = [
        schemas.OrderResponse(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            products=[
                schemas.ProductResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                )
                for product in order.products
            ],
        )
        for order in orders
    ]

    return order_responses

def update_orders(
    db: Session,
    order_id: int,
    order: schemas.OrderUpdate,
    current_user: schemas.UserResponse,
):
    order_update = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order_update:
        raise HTTPException(status_code=404, detail="Order not found")

    order_update.status = order.status
    db.commit()
    db.refresh(order_update)

    return schemas.OrderResponse(
        id=order_update.id,
        user_id=order_update.user_id,
        status=order_update.status,
        products=(
            [schemas.ProductResponse.model_validate(p) for p in order_update.products]
            if order_update.products
            else []
        ),
    )

def get_order(db: Session, order_id: int, current_user: schemas.UserResponse):
    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id, models.Order.user_id == current_user.id)
        .options(joinedload(models.Order.products))  # Eagerly load products
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return schemas.OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        products=[
            schemas.ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
            )
            for product in order.products
        ],
    )

def delete_order(db: Session, order_id: int, current_user: schemas.UserResponse):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # ✅ Ensure the order belongs to the current user
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this order")

    db.delete(order)
    db.commit()
    
    return {"message": "Order deleted successfully"}
