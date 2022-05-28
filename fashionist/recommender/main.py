import torch
import torchvision
from PIL import Image

from .fashion_compatibility_mcn.model import CompatModel
from .fashion_compatibility_mcn.utils import (
    Category,
    CategoryMean,
    defect_detect,
    get_category_options,
    get_polyvore_dataloader,
    item_diagnosis,
    load_images_from_ids,
    plot_results,
    retrieve_sub,
    vec2mat,
)


def update_output(
    imgs_dir,
    metadata_dir,
    test_dataset,
    num_max_tries,
    product_ids,
    category_filter,
    model,
    transforms,
    device,
    seed = None,
) -> tuple[list[str], list[str]]:
    '''
    Update outfit based on user inputs.

    Args:
        imgs_dir: directory containing the Polyvore Dataset.
        metadata_dir: directory containing essential metadata to run
            the model.
        test_dataset: PyTorch DataLoader to select products from.
        num_max_tries: maximum number of attempts to search for
            products per category.
        product_ids: list of product IDs in the following format:
            Polyvore image: `119704139_1`, where the first digits are
            the instance of the dataset and the last digit is the image
            for this instance.
            Mean image: if you do not want to use a category, you can
            pass the mean image for it. E.g., for 'upper', you would use
            `CategoryMean.upper.value`.
            category_filter: list of categories to exclude from
            recommendation. E.g., if you wish to exclude 'bottom',
            pass `[Category.bottom.value]`.
        model: the model to compute the compatibility score.
        transforms: Torchvision transforms.
        device: Torch device used for computation.
        seed: seed to sample random numbers with.

    Return:
        new_paths: paths to substituted images. Always has 5 items.
        old_paths: paths to original images. Always has 5 items.
    '''
    # load image data
    imgs_tensor, old_paths = load_images_from_ids(product_ids, imgs_dir,
            metadata_dir, transforms, device)

    # compute relationship between products and their match scores
    relation, score = defect_detect(
        img=imgs_tensor,
        model=model,
        device=device,
    )
    relation = relation.squeeze()

    # filter out selections. First, remove unselected items (mean images)
    selection = [i for i, j in enumerate(product_ids) if 'mean' not in j]
    # next, remove user constraints (fixed products)
    selection = [i for i in selection if i not in category_filter]

    # get sorted order of worst items
    result, order = item_diagnosis(
        relation=relation,
        select=selection,
        device=device,
    )

    # find substitutions
    best_score, best_img_path = retrieve_sub(
        x=imgs_tensor,
        test_dataset=test_dataset,
        model=model,
        select=selection,
        order=order,
        device=device,
        try_most=num_max_tries,
        seed=seed,
    )

    # get new paths based on substitutions
    new_paths = old_paths.copy()
    for i, part in enumerate(Category._member_names_):
        if part in best_img_path.keys():
            fname = best_img_path[part]
            new_paths[i] = fname

    print(f'Original score: {score:.4f}')
    print(f'Revised score: {best_score:.4f}')

    return new_paths, old_paths


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    img_root = '/home/martin/Downloads/polyvore-images/images/'
    metadata_root = '/home/martin/workspace/Hackathon-TeiaLabs/res/metadata/'
    weights_path = '/home/martin/workspace/Hackathon-TeiaLabs/res/model_train_relation_vse_type_cond_scales.pth'
    num_max_tries = 25

    test_dataset, _ = get_polyvore_dataloader(split='test', imgs_dir=img_root,
            metadata_dir=metadata_root,)

    model = CompatModel(embed_size=1000, need_rep=True, vocabulary=2757)
    model.to(device)
    weights = torch.load(weights_path, map_location='cpu')
    model.load_state_dict(weights)
    model.eval()

    options = get_category_options(img_root, metadata_root)

    # PICK IMAGES HERE
    ids = [
        options[Category.upper.name][0]['id'],
        options[Category.bottom.name][0]['id'],
        options[Category.shoe.name][0]['id'],
        CategoryMean.bag.value,
        # options[Category.bag.name][0]['id'],
        options[Category.accessory.name][0]['id'],
    ]

    # EXCLUDE CATEGORIES HERE
    category_filter = [
        Category.upper.value,
        Category.bottom.value,
        # Category.shoe.value,
        # Category.bag.value,
        # Category.accessory.value,
    ]

    new_paths, old_paths = update_output(
        imgs_dir=img_root,
        metadata_dir=metadata_root,
        test_dataset=test_dataset,
        num_max_tries=num_max_tries,
        product_ids=ids,
        category_filter=category_filter,
        model=model,
        transforms=test_dataset.transform,
        device=device,
        seed=None,
    )

    plot_results(old_paths, new_paths, test_dataset.transform)



if __name__ == '__main__':
    main()
