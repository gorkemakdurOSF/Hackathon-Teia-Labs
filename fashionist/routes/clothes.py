from typing import List, Optional

from fastapi import APIRouter, Response, HTTPException

from ..models.clothes import Clothes, UpdateClothes
from ..models.wardrobe import Wardrobe

router = APIRouter(prefix='/wardrobe/{wardrobe_id}/clothes')


@router.get('/', status_code=200, response_model=List[Clothes])
async def get_all_wardrobe_clothes(
        wardrobe_id: str,
        tags: Optional[List[str]],
        offset: int,
        limit: int
):
    wardrobe = (await Wardrobe.read(_id=wardrobe_id))[0]
    filters = {"$and": [{"_id": {"$in": wardrobe.clothes}}]}
    if tags:
        filters["$and"].append({"tags": tags})
    else:
        filters = filters["$and"][0]

    clothes = await Clothes.read(
        offset=offset,
        limit=limit,
        kwargs=filters
    )

    return clothes


@router.get('/{_id}', status_code=200, response_model=Clothes)
async def get_wardrobe_clothes(wardrobe_id: str, _id: str):
    wardrobe = (await Wardrobe.read(_id=wardrobe_id))[0]
    clothes = await Clothes.read(
        kwargs={"$and": [{"_id": {"$in": wardrobe.clothes}}, {"_id": _id}]}
    )

    return clothes[0]


@router.post('/', status_code=201, response_model=Clothes)
async def create_wardrobe_clothes(wardrobe_id: str, clothes: Clothes):
    clothes_id = await Clothes.create(clothes)
    wardrobe = (await Wardrobe.read(_id=wardrobe_id))[0]
    wardrobe.clothes.append(clothes_id)
    await Wardrobe.update(wardrobe_id, wardrobe)

    return clothes


@router.put('/{_id}', status_code=204, response_class=Response)
async def update_wardrobe_clothes(
        wardrobe_id: str,
        _id: str,
        clothes: UpdateClothes
):
    wardrobe = (await Wardrobe.read(_id=wardrobe_id))[0]
    clothes_on_database = await Clothes.read(
        kwargs={"$and": [{"_id": {"$in": wardrobe.clothes}}, {"_id": _id}]}
    )
    if not clothes_on_database:
        return HTTPException(status_code=404, detail="Clothes not found")

    await Clothes.update(_id, clothes)


@router.delete('/{_id}', status_code=204, response_class=Response)
async def delete_wardrobe_clothes(wardrobe_id: str, _id: str):
    wardrobe = (await Wardrobe.read(_id=wardrobe_id))[0]
    clothes_on_database = await Clothes.read(
        kwargs={"$and": [{"_id": {"$in": wardrobe.clothes}}, {"_id": _id}]}
    )
    if not clothes_on_database:
        return HTTPException(status_code=404, detail="Clothes not found")

    await Clothes.delete(_id)
