import json
import os
import random
from enum import Enum
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torchvision
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from .polyvore_dataset import CategoryDataset, collate_fn


class Category(Enum):
    '''
    Enumeration of supported clothing categories.
    '''
    upper = 0
    bottom = 1
    shoe = 2
    bag = 3
    accessory = 4


class CategoryMean(Enum):
    '''
    Enumeration of supported clothing categories and their respective
    mean image names
    '''
    upper = 'upper_mean'
    bottom = 'bottom_mean'
    shoe = 'shoe_mean'
    bag = 'bag_mean'
    accessory = 'accessory_mean'


def load_images_from_ids(
    img_ids: list[str],
    imgs_dir: str,
    metadata_dir: str,
    transform: torchvision.transforms.Compose,
    device: torch.device,
) -> tuple[torch.Tensor, list[str]]:
    '''
    Loads images from Polyvore Dataset (or mean images if unspecified).

    Args:
        img_ids: list of image IDs (if you want to exclude a category,
        pass its corresponding mean image name (e.g., for upper, use
        `upper_mean`).
        imgs_dir: directory containing the Polyvore Dataset.
        metadata_dir: directory containing essential metadata to run
            the model.
        transform: Torchvision transforms.
        device: Torch device used for computation.

    Return:
        final_tensor: PyTorch Tensor with all images [1, 5, H, W].
        paths: list of image paths.
    '''
    final_tensor = []
    paths = []
    for img_id in img_ids:
        if 'mean' in img_id:
            # load mean image
            img_file = img_id.split('_')[0] + '.png'
            img_path = os.path.join(metadata_dir, img_file)
        else:
            img_path = os.path.join(imgs_dir, *img_id.split('_')) + '.jpg'

        img = Image.open(img_path).convert('RGB')
        img = transform(img)
        final_tensor.append(img)
        paths.append(img_path)

    final_tensor = torch.stack(final_tensor)
    final_tensor = final_tensor.unsqueeze(0)
    final_tensor = final_tensor.to(device)
    return final_tensor, paths


def get_category_options(
    imgs_dir: str,
    metadata_dir: str,
    max_instances: int = 100,
) -> dict[str, list]:
    '''
    Get products for each category from the Polyvore Dataset.

    Args:
        imgs_dir: directory containing the Polyvore Dataset.
        metadata_dir: directory containing essential metadata to run
            the model.
        max_instances: maximum number of instances to collect.

    Return:
        options (dict): dictionary with products for each category.
    '''
    options = {c: [] for c in Category._member_names_}

    json_file_path = os.path.join(metadata_dir,
            'test_no_dup_with_category_3more_name.json')
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)
    json_data = {k:v for k, v in json_data.items() \
            if os.path.exists(os.path.join(imgs_dir, k))}

    for cnt, (iid, outfit) in enumerate(json_data.items()):
        if cnt > max_instances:
            break

        for category, value in outfit.items():
            label = os.path.join(iid, str(outfit[category]['index']))
            path = os.path.join(imgs_dir, label) + ".jpg"
            options[category].append({
                'id': label.replace('/', '_'),
                'outfit_id': label.split('/')[0],
                'path': path,
                'value': value,
            })

    return options


def defect_detect(
    img: torch.Tensor,
    model: nn.Module,
    device: torch.device,
    normalize: bool = True,
) -> tuple[torch.Tensor, float]:
    '''
    Compute the gradients of each element in the comparison matrices
    to approximate the problem of each input.

    Args:
        img: images of shape (B, 3, 224, 224).
        model: the model to compute the compatibility score.
        device: Torch device used for computation.
        normalize: whether to normalize the relation results or not.

    Return:
        relation (torch.Tensor): gradients on comparison matrix.
            Shape: [1, 60].
        out (float): prediction score.
    '''
    relation = None

    # register hook for comparison matrix
    def func_r(module, grad_in, grad_out):
        nonlocal relation
        # relation = grad_in[1].detach()
        relation = grad_in[0].detach()

    for name, module in model.named_modules():
        if name == 'predictor.0':
            # module.register_backward_hook(func_r)
            module.register_full_backward_hook(func_r)

    # forward
    out = model._compute_score(img)
    out = out[0]

    # backward
    one_hot = torch.FloatTensor([[-1]]).to(device)
    model.zero_grad()
    out.backward(gradient=one_hot, retain_graph=True)

    if normalize:
        relation = relation / (relation.max() - relation.min())
    relation += 1e-3

    return relation, out.item()


def item_diagnosis(
    relation: torch.Tensor,
    select: list,
    device: torch.device,
) -> tuple[list, list]:
    '''
    Outputs the most incompatible item in an outfit.

    Args:
        relation: gradients on comparison matrix (shape [60]).
        select: list of selected item indices, e.g., (0, 2, 3) means
            select these 3 items (of 5 total items in the outfit).
        device: Torch device used for computation.

    Return:
        result (list): diagnosis value of each item.
        order (list): the indices of items ordered by their importance.
    '''
    mats = vec2mat(relation, select, device)
    # remove main diagonal for each matrix
    for m in mats:
        mask = torch.eye(*m.shape, dtype=bool).to(device)
        m.masked_fill_(mask, 0)

    # sum individual matrices
    result = torch.cat(mats).sum(dim=0)
    # get matrices ordering
    order = [i for i, j in sorted(enumerate(result), key=lambda x:x[1],
        reverse=True)]

    return result, order


def vec2mat(
    relation: torch.Tensor,
    select: list,
    device: torch.device,
) -> list:
    '''
    Convert relation vector to 4 matrix, which corresponds to 4 layers
    in the backbone CNN.

    Args:
        relation: torch.Tensor of shape [60,]
        select: list of selected item indices, e.g., (0, 2, 3) means
            select 3 items (of 5 total items in the outfit).
        device: Torch device used for computation.

    Return:
        mats (list): list of matrices (torch.Tensor).
    '''
    mats = []
    for idx in range(4):
        mat = torch.zeros(5, 5).to(device)
        mat[np.triu_indices(5)] = relation[15*idx:15*(idx+1)]
        mat += torch.triu(mat, 1).transpose(0, 1)
        mat = mat[select, :]
        mat = mat[:, select]
        mats.append(mat)
    return mats


def retrieve_sub(
    x: torch.Tensor,
    test_dataset: torch.utils.data.DataLoader,
    model: nn.Module,
    select: list,
    order: list,
    device: torch.device,
    try_most: int = 10,
    seed: int = None,
) -> tuple[float, dict]:
    '''
    Retrieve an item from `test_dataset` to substitue the worst item.

    Args:
        x: Tensor containing the images for each product category.
        test_dataset: PyTorch DataLoader to select products from.
        model: the model to compute the compatibility score.
        select: which parts to check for substitutions.
        order: the indices of items ordered by their importance.
        device: Torch device used for computation.
        try_most: maximum number of attempts to search for products per
            category.
        seed: seed to sample random numbers with.

    Return:
        best_score (float): score obtained after substitutions.
        best_img_path (dict): dictionary containing information about
            which categories suffered substitutions and their respective
            image paths.
    '''
    if seed:
        random.seed(seed)

    all_names = {c.value: c.name for c in Category}
    best_score = -1
    best_img_path = dict()

    # iterate through categories based on their importance
    for o in order:
        if best_score > 0.9:
            break

        # get product category
        problem_part_idx = select[o]
        problem_part = all_names[problem_part_idx]

        # sample random products from dataset
        for outfit in random.sample(test_dataset.data, try_most):
            if best_score > 0.9:
                break

            # TODO: improve this, currently we sample images from any
            # category, which means that if we are unlucky, we may never
            # select pieces of clothing from this category.
            if problem_part in outfit[1]:
                # load image
                img_path = os.path.join(test_dataset.root_dir, outfit[0],
                        str(outfit[1][problem_part]['index'])) + '.jpg'
                img = Image.open(img_path).convert('RGB')
                img = test_dataset.transform(img).to(device)
                x[0][problem_part_idx] = img

                # compute model scores
                with torch.no_grad():
                    out = model._compute_score(x)
                    score = out[0]

                # if we get a better score for this product, substitute
                if score.item() > best_score:
                    best_score = score.item()
                    best_img_path[problem_part] = img_path

        # if we replaced a product, substitute product image for inference
        if problem_part in best_img_path:
            img = Image.open(best_img_path[problem_part]).convert('RGB')
            x[0][problem_part_idx] = test_dataset.transform(img).to(device)

            print(f'Problem_part: {problem_part}')
            print(f'Best substitution: {best_img_path[problem_part]}')
            print(f'Score after substitution: {best_score:.4f}')
            print()

    return best_score, best_img_path


def get_polyvore_dataloader(
    split: str,
    imgs_dir: str,
    metadata_dir: str,
    batch_size: int = 16,
    img_size: int = 224,
    use_mean_img: bool = True,
    neg_samples: bool = True,
    num_workers: int = 1,
    collate_fn: Callable = collate_fn,
) -> tuple[torch.utils.data.Dataset, torch.utils.data.DataLoader]:
    '''
    Return PyTorch DataLoader for Polyvore Dataset.

    Args:
        split: which data split to use (train | valid | test).
        imgs_dir: directory containing Polyvore images.
        metadata_dir: directory containing essential metadata to run
            the model.
        batch_size: batch size.
        img_size: image size.
        use_mean_img: whether to use mean image to fill blanks or not.
        neg_samples: whether to generate negative sampled outfits or not.
        num_workers: number of threads to load data.
        collate_fn: custom collate function.

    Return:
        dataset (torch.utils.data.Dataset): PyTorch Dataset.
        loader (torch.utils.data.DataLoader): PyTorch DataLoader.
    '''
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((img_size, img_size)),
        torchvision.transforms.ToTensor(),
    ])

    if split == 'train':
        data_file = 'train_no_dup_with_category_3more_name.json'
        shuffle = True
    elif split == 'valid':
        data_file = 'valid_no_dup_with_category_3more_name.json'
        shuffle = False
    elif split == 'test':
        data_file = 'test_no_dup_with_category_3more_name.json'
        shuffle = False

    dataset = CategoryDataset(
        root_dir=imgs_dir,
        data_dir=metadata_dir,
        transform=transform,
        use_mean_img=use_mean_img,
        data_file=data_file,
    )

    loader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=4,
        collate_fn=collate_fn,
    )

    return dataset, loader


def plot_results(old_paths, new_paths, transform):
    all_paths = old_paths + new_paths
    all_imgs_tensor = [transform(Image.open(p).convert('RGB')) \
            for p in all_paths]
    all_imgs_grid = torchvision.utils.make_grid(all_imgs_tensor, nrow=5)
    all_imgs_grid = all_imgs_grid.permute([1, 2, 0])

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 2], sharex=True)
    ax.imshow(all_imgs_grid)

    fig.tight_layout()

    plt.show()
