import json
import shopify

from .settings import SETTINGS


def create_session():
    shopify.Session.setup(api_key=SETTINGS.API_KEY, secret=SETTINGS.API_SECRET_KEY)

    session = shopify.Session(SETTINGS.SHOP_URL, SETTINGS.API_VERSION, SETTINGS.TOKEN)
    shopify.ShopifyResource.activate_session(session)


def execute_graph_call(query):
    out = json.loads(shopify.GraphQL().execute(query))
    return out.get("data")


def quit_session():
    shopify.ShopifyResource.clear_session()
