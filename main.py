# main.py
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
import os
import shopify
import requests
from typing import List
from datetime import datetime

from routes import orders, customers, shopify  # Include shopify routes
from models import Customer, Order
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from schemas import CustomerSchema, OrderSchema, ProductSchema

load_dotenv()

app = FastAPI(title="Shopify FastAPI Integration")

# Include Routers
app.include_router(orders.router)
app.include_router(customers.router)
app.include_router(shopify.router)  # Include the shopify router

# OAuth Routes (if applicable)
@app.get("/auth/install")
def install_app(request: Request):
    # Existing OAuth implementation
    return {"detail": "Install endpoint"}

@app.get("/auth/callback")
def auth_callback(request: Request):
    # Existing OAuth implementation
    return {"detail": "OAuth callback processed successfully"}

# Exception Handlers (Optional but Recommended)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
