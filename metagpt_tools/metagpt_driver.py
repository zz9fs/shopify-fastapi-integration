# metagpt_driver.py

from metagpt import MetaGPTAgent  # Hypothetical import
from metagpt_tools.register_tools import register_tools

def main():
    # Initialize the MetaGPT agent
    agent = MetaGPTAgent()
    
    # Register the Shopify tool
    register_tools(agent)
    
    # Example interaction: Create a customer
    customer = agent.use_tool(
        tool_name="ShopifyIntegrationTool",
        function_name="create_customer",
        first_name="Alice",
        last_name="Wonderland",
        email="alice.wonderland@example.com",
        phone="123-456-7890"
    )
    print("Created Customer:", customer)
    
    # Example interaction: Fetch products from Shopify
    products = agent.use_tool(
        tool_name="ShopifyIntegrationTool",
        function_name="fetch_shopify_products"
    )
    print("Shopify Products:", products)

if __name__ == "__main__":
    main()




# Created Customer: {
#     "id": 301,
#     "first_name": "Alice",
#     "last_name": "Wonderland",
#     "email": "alice.wonderland@example.com",
#     "phone": "123-456-7890",
#     "created_at": "2024-12-14T10:00:00"
# }
# Shopify Products: {
#     "products": [
#         {
#             "id": 987654321,
#             "title": "MetaGPT Product",
#             "body_html": "<strong>Excellent product!</strong>",
#             "vendor": "MetaVendor",
#             "product_type": "MetaType",
#             "created_at": "2024-01-10T00:00:00-05:00",
#             "handle": "metagpt-product",
#             "updated_at": "2024-01-11T00:00:00-05:00",
#             "published_at": "2024-01-12T00:00:00-05:00",
#             "template_suffix": "",
#             "tags": "meta,gpt,product"
#         }
#     ]
# }
