from typing import List, Optional

from fastapi import APIRouter, Response, HTTPException

from ..models import PyObjectId
from ..models.outfit import Outfit, UpdateOutfit
from ..models.wardrobe import Wardrobe
from ..models.clothes import Clothes

router = APIRouter(prefix='/outfits')


@router.get('/', status_code=200, response_model=List[Outfit])
async def get_all_outfit(
        tags: Optional[List[str]] = None,
        wardrobe_id: Optional[str] = None,
        offset: int = 0,
        limit: int = 100
):
    filters = {"$and": []}
    if wardrobe_id:
        wardrobe = (await Wardrobe.read(kwargs={"_id": wardrobe_id}))[0]
        filters["$and"].append({"_id": {"$in": wardrobe.outfits}})

    if tags:
        filters["$and"].append({"tags": tags})

    if not filters["$and"]:
        return await Outfit.read(offset=offset, limit=limit)

    return await Outfit.read(
        offset=offset,
        limit=limit,
        kwargs=filters
    )


@router.get('/{_id}', status_code=200, response_model=Outfit)
async def get_outfit(_id: str, wardrobe_id: Optional[str] = None):
    _id = PyObjectId(_id)

    if wardrobe_id:
        wardrobe = (await Wardrobe.read(kwargs={"_id": PyObjectId(wardrobe_id)}))[0]
        filters = {"$and": [{"_id": {"$in": wardrobe.outfits}}, {"_id": _id}]}
    else:
        filters = {"_id": _id}

    outfit = await Outfit.read(kwargs=filters)
    if not outfit:
        raise HTTPException(status_code=404, detail="Clothes not found")

    return outfit[0]


@router.post('/', status_code=201, response_model=Outfit)
async def create_outfit(outfit: Outfit):
    outfit.clothes = list(map(PyObjectId, outfit.clothes))
    clothes = await Clothes.read(kwargs={"_id": {"$in": outfit.clothes}})
    if len(outfit.clothes) < len(clothes):
        raise HTTPException(status_code=404, detail="Certain clothes were not found")

    tags = []
    for c in clothes:
        tags.extend(c.get("tags"))

    outfit.tags.extend(tags)
    await Outfit.create(outfit)
    return outfit


@router.put('/{_id}', status_code=204, response_class=Response)
async def update_outfit(_id: str, outfit: UpdateOutfit):
    await Outfit.update(PyObjectId(_id), outfit)


@router.delete('/{_id}', status_code=204, response_class=Response)
async def delete_outfit(_id: str, wardrobe_id: Optional[str] = None):
    _id = PyObjectId(_id)

    if wardrobe_id:
        wardrobe_id = PyObjectId(wardrobe_id)

        wardrobe = (await Wardrobe.read(kwargs={"_id": wardrobe_id}))[0]
        outfit_on_database = await Outfit.read(
            kwargs={"$and": [{"_id": {"$in": wardrobe.outfits}}, {"_id": _id}]}
        )
        if not outfit_on_database:
            return HTTPException(status_code=404, detail="Clothes not found on wardrobe")

    await Outfit.delete(_id)
