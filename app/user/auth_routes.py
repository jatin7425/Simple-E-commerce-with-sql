import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from ..user.auth import get_current_user
from ..models import User, Order, Product
from app.schemas import UserCreate, UserResponse, Token,  UserResponse, OrderResponse, ProductResponse
from .auth import create_access_token, get_current_user, verify_password, get_password_hash

from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and generate JWT token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def get_user_me(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of the currently authenticated user along with orders."""
    
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch user's orders
    user_orders = db.query(Order).filter(Order.user_id == user.id).all()

    print(user_orders)

    # Prepare orders with product details
    orders_with_products = []
    for order in user.orders:  # Directly access the related orders
        products = order.products  # Directly access the related products

        order_data = OrderResponse(
            id=order.id,
            user_id=order.user_id,
            products=[
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price
                ) for product in products
            ]
        )
        orders_with_products.append(order_data)
        
        
    # Return user with orders
    return UserResponse(
        id=user.id,
        username=user.username,
        orders=orders_with_products  # Attach orders with product details
    )
