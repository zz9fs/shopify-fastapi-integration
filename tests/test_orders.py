# tests/test_orders.py
import pytest
from fastapi import status

def test_create_order(client, setup_and_teardown):
    # First, create a customer to associate with the order
    customer_response = client.post(
        "/customers/",
        json={
            "first_name": "Order",
            "last_name": "Tester",
            "email": "order.tester@example.com",
            "phone": "222-333-4444"
        }
    )
    customer_id = customer_response.json()["id"]
    
    response = client.post(
        "/orders/",
        json={
            "order_number": "ORD123456",
            "customer_id": customer_id,
            "total_amount": 99.99,
            "status": "pending"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["order_number"] == "ORD123456"
    assert data["customer_id"] == customer_id
    assert "id" in data
    assert "created_at" in data

def test_create_order_duplicate_order_number(client, setup_and_teardown):
    # Create a customer
    customer_response = client.post(
        "/customers/",
        json={
            "first_name": "Duplicate",
            "last_name": "Order",
            "email": "duplicate.order@example.com",
            "phone": "555-666-7777"
        }
    )
    customer_id = customer_response.json()["id"]
    
    # First order creation
    client.post(
        "/orders/",
        json={
            "order_number": "ORD_DUPLICATE",
            "customer_id": customer_id,
            "total_amount": 150.00,
            "status": "completed"
        }
    )
    
    # Attempt duplicate order creation
    response = client.post(
        "/orders/",
        json={
            "order_number": "ORD_DUPLICATE",
            "customer_id": customer_id,
            "total_amount": 200.00,
            "status": "processing"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Order number already exists"

def test_get_orders(client, setup_and_teardown):
    # Create a customer
    customer_response = client.post(
        "/customers/",
        json={
            "first_name": "OrderList",
            "last_name": "User",
            "email": "orderlist.user@example.com",
            "phone": "888-999-0000"
        }
    )
    customer_id = customer_response.json()["id"]
    
    # Create multiple orders
    orders = [
        {
            "order_number": "ORD1001",
            "customer_id": customer_id,
            "total_amount": 50.00,
            "status": "completed"
        },
        {
            "order_number": "ORD1002",
            "customer_id": customer_id,
            "total_amount": 75.50,
            "status": "pending"
        }
    ]
    for order in orders:
        client.post("/orders/", json=order)
    
    response = client.get("/orders/?skip=0&limit=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["order_number"] == "ORD1001"
    assert data[1]["order_number"] == "ORD1002"

def test_get_order_by_id(client, setup_and_teardown):
    # Create a customer
    customer_response = client.post(
        "/customers/",
        json={
            "first_name": "Specific",
            "last_name": "Order",
            "email": "specific.order@example.com",
            "phone": "333-444-5555"
        }
    )
    customer_id = customer_response.json()["id"]
    
    # Create an order
    order_response = client.post(
        "/orders/",
        json={
            "order_number": "ORD_SPECIFIC",
            "customer_id": customer_id,
            "total_amount": 120.00,
            "status": "processing"
        }
    )
    order_id = order_response.json()["id"]
    
    # Retrieve the order by ID
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == status.HTTP_200_OK
    data = get_response.json()
    assert data["order_number"] == "ORD_SPECIFIC"

def test_get_nonexistent_order(client, setup_and_teardown):
    response = client.get("/orders/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"
