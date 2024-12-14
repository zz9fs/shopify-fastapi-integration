# tests/test_customers.py
import pytest
from fastapi import status
from sqlalchemy.orm import Session

from schemas import CustomerCreate

def test_create_customer(client, setup_and_teardown):
    response = client.post(
        "/customers/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "phone": "123-456-7890"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test.user@example.com"
    assert "id" in data
    assert "created_at" in data

def test_create_customer_duplicate_email(client, setup_and_teardown):
    # First creation
    client.post(
        "/customers/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "duplicate@example.com",
            "phone": "123-456-7890"
        }
    )
    # Attempt duplicate creation
    response = client.post(
        "/customers/",
        json={
            "first_name": "Another",
            "last_name": "User",
            "email": "duplicate@example.com",
            "phone": "098-765-4321"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

def test_get_customers(client, setup_and_teardown):
    # Create multiple customers
    customers = [
        {
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com",
            "phone": "111-222-3333"
        },
        {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "phone": "444-555-6666"
        }
    ]
    for customer in customers:
        client.post("/customers/", json=customer)
    
    response = client.get("/customers/?skip=0&limit=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "alice@example.com"
    assert data[1]["email"] == "bob@example.com"

def test_get_customer_by_id(client, setup_and_teardown):
    # Create a customer
    response = client.post(
        "/customers/",
        json={
            "first_name": "Charlie",
            "last_name": "Chocolate",
            "email": "charlie@example.com",
            "phone": "777-888-9999"
        }
    )
    customer_id = response.json()["id"]
    
    # Retrieve the customer by ID
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == status.HTTP_200_OK
    data = get_response.json()
    assert data["email"] == "charlie@example.com"

def test_get_nonexistent_customer(client, setup_and_teardown):
    response = client.get("/customers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Customer not found"
