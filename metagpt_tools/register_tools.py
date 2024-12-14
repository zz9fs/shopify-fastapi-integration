# metagpt_tools/register_tools.py

from metagpt_tools.shopify_tool import ShopifyTool

def register_tools(meta_gpt_instance):
    shopify_tool = ShopifyTool(base_url="http://127.0.0.1:8000", auth_token="your_auth_token_here")
    meta_gpt_instance.register_tool("ShopifyIntegrationTool", shopify_tool)
