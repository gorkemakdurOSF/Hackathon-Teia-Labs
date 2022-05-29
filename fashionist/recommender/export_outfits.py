import argparse
import json
import os
import random
import time

import shopify
from tqdm import tqdm
from shopify import Session, ShopifyResource, Product

from .fashion_compatibility_mcn.utils import (
    Category,
    get_category_options,
    get_polyvore_dataloader,
)


def main(args):
    products = export_outfits(args.imgs_dir, args.metadata_dir,
            args.num_outfits)
    send_products_to_shopify(products, args.shopify_api_key,
            args.shopify_api_secret, args.shopify_store_url,
            args.shopify_access_token)


def export_outfits(
    imgs_dir,
    metadata_dir,
    num_outfits,
):
    dataset, loader = get_polyvore_dataloader(
        split='test',
        imgs_dir=imgs_dir,
        metadata_dir=metadata_dir,
    )

    options = get_category_options(
        imgs_dir,
        metadata_dir,
        max_instances=num_outfits,
    )

    products = {}
    for category_name in Category._member_names_:
        for outfit in options[category_name]:
            products[outfit['id']] = outfit

    return products


def product_exists(
    product_id,
):
    products = shopify.Product.find()
    for product in products:
        m = product.metafields()
        curr_id = json.loads(m[0].value)['id']
        if curr_id == product_id:
            return True

    return False


def send_products_to_shopify(
    products,
    api_key,
    api_secret,
    store_url,
    access_token,
):
    Session.setup(api_key=api_key, secret=api_secret)
    session = Session(store_url, '2022-04', access_token)
    ShopifyResource.activate_session(session)

    # shuffle products
    # prod_list = list(products.items())
    # random.shuffle(prod_list)
    # products = dict(prod_list)

    for prod_id, prod_metadata in tqdm(products.items()):
        tqdm.write(f'Adding {prod_id}')
        if product_exists(prod_id):
            tqdm.write('Product already exists')
            time.sleep(1)
            continue

        product = Product()
        product.title = prod_metadata['value']['name']
        product.save()

        product.add_metafield(
            shopify.Metafield({
                'type': 'json', 
                'namespace': 'outfit', 
                'key': 'info',
                'value': json.dumps(prod_metadata)
            })
        )
        success = product.save()
        if not success:
            print(f'Problem adding {prod_id}')
            continue

        # prod = shopify.Product.find(product.id)
        # m = prod.metafields()
        # print(json.loads(m[0].value)['id'])

        image = shopify.Image({'product_id': product.id})

        with open(prod_metadata['path'], 'rb') as f:
            image.attach_image(f.read(), filename=product.id)

        image.save()
        time.sleep(1)

    ShopifyResource.clear_session()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--imgs_dir', type=str, required=True,
            help='Path to directory containing Polyvore Dataset images.')
    parser.add_argument('--metadata_dir', type=str, required=True,
            help='Path to directory containing Polyvore Dataset images.')

    parser.add_argument('--outfit_json', type=str, required=True,
            help='Path to JSON containing Polyvore Dataset outfits.')
    parser.add_argument('--num_outfits', type=int, required=True,
            help='Number of outfits to export.')

    parser.add_argument('--shopify_access_token', type=str, required=True,
            help='Shopify access token.')
    parser.add_argument('--shopify_api_key', type=str, required=True,
            help='Shopify API key.')
    parser.add_argument('--shopify_api_secret', type=str, required=True,
            help='Shopify API secret.')
    parser.add_argument('--shopify_store_url', type=str, required=True,
            help='Shopify store URL.')

    args = parser.parse_args()
    main(args)
