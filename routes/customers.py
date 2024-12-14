# routes/customers.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from models import Customer
from database import get_db
from schemas import CustomerSchema, CustomerCreate

router = APIRouter()

@router.get("/customers/", response_model=List[CustomerSchema])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.post("/customers/", response_model=CustomerSchema)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/customers/{customer_id}", response_model=CustomerSchema)
def read_customer(
    customer_id: int = Path(..., title="The ID of the customer to retrieve", ge=1),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific customer by their ID.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
