from fastapi import FastAPI
from .database import engine, Base
from .product.prod_routes import router as Prod_router
from .user.auth_routes import router as auth_router
from .orders.order_routes import router as order_router

app = FastAPI(openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")

# Create DB tables
Base.metadata.create_all(bind=engine)
app.include_router(Prod_router)
app.include_router(auth_router)
app.include_router(order_router)
