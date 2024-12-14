# metagpt_tools/shopify_tool.py

import requests

class ShopifyTool:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json"
        }
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
    
    def create_customer(self, first_name, last_name, email, phone):
        url = f"{self.base_url}/customers/"
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_customers(self, skip=0, limit=10):
        url = f"{self.base_url}/customers/"
        params = {"skip": skip, "limit": limit}
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_customer(self, customer_id):
        url = f"{self.base_url}/customers/{customer_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
    def create_order(self, order_number, customer_id, total_amount, status):
        url = f"{self.base_url}/orders/"
        payload = {
            "order_number": order_number,
            "customer_id": customer_id,
            "total_amount": total_amount,
            "status": status
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_orders(self, skip=0, limit=10):
        url = f"{self.base_url}/orders/"
        params = {"skip": skip, "limit": limit}
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_order(self, order_id):
        url = f"{self.base_url}/orders/{order_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
    def fetch_shopify_products(self):
        url = f"{self.base_url}/shopify/products/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
