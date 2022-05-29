import argparse
import json
import os

from .fashion_compatibility_mcn.utils import (
    Category,
    get_category_options,
    get_polyvore_dataloader,
)


def export_outfits(args):
    dataset, loader = get_polyvore_dataloader(
        split='test',
        imgs_dir=args.imgs_dir,
        metadata_dir=args.metadata_dir,
    )

    options = get_category_options(
        args.imgs_dir,
        args.metadata_dir,
        max_instances=args.num_outfits,
    )

    products = {}
    for category_name in Category._member_names_:
        for outfit in options[category_name]:
            products[outfit['id']] = outfit

    return products



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

    args = parser.parse_args()
    export_outfits(args)
