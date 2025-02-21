from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import prod_crud
from ..database import get_db
from ..user.auth import get_current_user
from .. import schemas


router = APIRouter(prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    return prod_crud.create_product(db, product)

@router.get("/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return prod_crud.get_products(db)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = prod_crud.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def get_product_by_id(product_id: int,product: schemas.ProductBase, db: Session = Depends(get_db)):
    product = prod_crud.update_product(db, product_id, product)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=schemas.ProductResponse)
def del_product(product_id: int, db: Session = Depends(get_db)):
    product = prod_crud.delete_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
