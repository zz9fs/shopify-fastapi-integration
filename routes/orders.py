# routes/orders.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from models import Order
from database import get_db
from schemas import OrderSchema, OrderCreate

router = APIRouter()

@router.get("/orders/", response_model=List[OrderSchema])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@router.post("/orders/", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_number == order.order_number).first()
    if db_order:
        raise HTTPException(status_code=400, detail="Order number already exists")
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/orders/{order_id}", response_model=OrderSchema)
def read_order(
    order_id: int = Path(..., title="The ID of the order to retrieve", ge=1),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific order by its ID.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
