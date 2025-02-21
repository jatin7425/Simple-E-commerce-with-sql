from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .. import models, schemas

def create_product(db: Session, prod: schemas.ProductBase):
    db_prod = models.Product(name=prod.name, description=prod.description, price=prod.price)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, prod: schemas.ProductBase):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        return {"error": "Product not found"}
    
    # Update only provided fields
    product.name = prod.name if prod.name and prod.name.lower not in ["string", ""] else product.name
    product.description = prod.description if prod.description.lower and prod.description not in ["string", ""] else product.description
    product.price = prod.price if prod.price and prod.price.lower != 0 else product.price

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return JSONResponse(content={"message": "Product deleted successfully"}, status_code=200)
    
    raise HTTPException(status_code=404, detail="Product not found")
