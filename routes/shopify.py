# routes/shopify.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import os

from database import get_db
from schemas import ProductSchema

router = APIRouter()

SHOPIFY_API_URL = "https://{shop}/admin/api/2023-10/products.json"

@router.get("/shopify/products/", response_model=dict)
def fetch_shopify_products(db: Session = Depends(get_db)):
    # Retrieve shop and access token from the database or environment
    shop = "mockshop.myshopify.com"  # Replace with dynamic retrieval
    access_token = "mock_access_token"  # Replace with dynamic retrieval
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    url = SHOPIFY_API_URL.format(shop=shop)
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch products from Shopify")
    
    return response.json()
