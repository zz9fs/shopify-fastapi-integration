# services/shopify_service.py
import shopify
import os
from dotenv import load_dotenv

load_dotenv()

class ShopifyService:
    def __init__(self):
        self.api_key = os.getenv('SHOPIFY_API_KEY')
        self.api_secret = os.getenv('SHOPIFY_API_SECRET')
        self.shop_name = os.getenv('SHOP_NAME')
        self.version = '2023-04'  # Shopify API version
        self.session = shopify.Session(self.shop_name, self.version, self.api_key, self.api_secret)
        shopify.ShopifyResource.activate_session(self.session)

    def get_orders(self):
        try:
            orders = shopify.Order.find(status='any', limit=250)
            return orders
        except Exception as e:
            raise Exception(f"Failed to retrieve orders: {str(e)}")

    def get_order(self, order_id):
        try:
            order = shopify.Order.find(order_id)
            if not order:
                raise Exception("Order not found")
            return order
        except Exception as e:
            raise Exception(f"Failed to retrieve order {order_id}: {str(e)}")

    def get_customers(self):
        try:
            customers = shopify.Customer.find(limit=250)
            return customers
        except Exception as e:
            raise Exception(f"Failed to retrieve customers: {str(e)}")

    def get_customer(self, customer_id):
        try:
            customer = shopify.Customer.find(customer_id)
            if not customer:
                raise Exception("Customer not found")
            return customer
        except Exception as e:
            raise Exception(f"Failed to retrieve customer {customer_id}: {str(e)}")

def get_shopify_service():
    return ShopifyService()
