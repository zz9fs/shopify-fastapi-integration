# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

# Sample mock data
mock_customers = {
    "customers": [
        {"id": 201, "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone": "123-456-7890", "created_at": "2024-12-13T22:00:00"},
        {"id": 202, "first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "phone": "234-567-8901", "created_at": "2024-12-13T22:05:00"}
    ]
}

mock_customer_detail = {
    "customer": {"id": 201, "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone": "123-456-7890", "created_at": "2024-12-13T22:00:00"}
}

def test_create_and_get_customer(client, setup_and_teardown):
    # Create a new customer
    response = client.post(
        "/customers/",
        json={
            "first_name": "Integration",
            "last_name": "Tester",
            "email": "integration.tester@example.com",
            "phone": "555-666-7777"
        }
    )
    assert response.status_code == 200
    created_customer = response.json()
    customer_id = created_customer["id"]
    
    # Retrieve the newly created customer
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["email"] == "integration.tester@example.com"

@patch('requests.post')
def test_shopify_oauth_callback(mock_post, client):
    # Mock the response from Shopify OAuth token request
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "access_token": "mock_access_token",
        "scope": "read_products,write_products",
        "associated_user_scope": "read_orders"
    }

    # Simulate OAuth callback with necessary query parameters
    response = client.get("/auth/callback", params={
        "code": "mock_code",
        "shop": "mockshop.myshopify.com",
        "state": "mock_state",
        "timestamp": "1612288000",
        "hmac": "mock_hmac"
    })

    # Assert the OAuth callback processed successfully
    assert response.status_code == 200
    assert response.json() == {"detail": "OAuth callback processed successfully"}

@patch('requests.get')
def test_shopify_api_fetch_products(mock_get, client):
    # Mock the response from Shopify API for fetching products
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "id": 123456789,
                "title": "Mock Product",
                "body_html": "<strong>Great product!</strong>",
                "vendor": "MockVendor",
                "product_type": "MockType",
                "created_at": "2024-01-01T00:00:00-05:00",
                "handle": "mock-product",
                "updated_at": "2024-01-02T00:00:00-05:00",
                "published_at": "2024-01-03T00:00:00-05:00",
                "template_suffix": "",
                "tags": "mock,product"
            }
        ]
    }

    # Assuming there's an endpoint that fetches products from Shopify
    response = client.get("/shopify/products/")

    # Assert the mocked Shopify API response is handled correctly
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 1
    assert data["products"][0]["title"] == "Mock Product"
