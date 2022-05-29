from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Response, HTTPException
from fastapi import UploadFile, Body

from ..models import PyObjectId
from ..models.clothes import Clothes, UpdateClothes
from ..models.wardrobe import Wardrobe

router = APIRouter(prefix='/clothes')


@router.get('/', status_code=200, response_model=List[Clothes])
async def get_all_clothes(
        tags: Optional[List[str]] = None,
        wardrobe_id: Optional[str] = None,
        offset: int = 0,
        limit: int = 100
):
    filters = {"$and": []}
    if wardrobe_id:
        wardrobe = (await Wardrobe.read(kwargs={"_id": wardrobe_id}))[0]
        filters["$and"].append({"_id": {"$in": wardrobe.clothes}})

    if tags:
        filters["$and"].append({"tags": tags})

    if not filters["$and"]:
        return await Clothes.read(offset=offset, limit=limit)

    return await Clothes.read(
        offset=offset,
        limit=limit,
        kwargs=filters
    )


@router.get('/{_id}', status_code=200, response_model=Clothes)
async def get_clothes(_id: str, wardrobe_id: Optional[str] = None):
    _id = PyObjectId(_id)

    if wardrobe_id:
        wardrobe = (await Wardrobe.read(kwargs={"_id": PyObjectId(wardrobe_id)}))[0]
        filters = {"$and": [{"_id": {"$in": wardrobe.clothes}}, {"_id": _id}]}
    else:
        filters = {"_id": _id}

    clothes = await Clothes.read(kwargs=filters)
    if not clothes:
        raise HTTPException(status_code=404, detail="Clothes not found")

    return clothes[0]


@router.post('/', status_code=201, response_model=Clothes)
async def create_clothes(value: UploadFile, tags: List[str]=Body()):
    clothes_id = await Clothes.create(Clothes(
        value=value.file.read(), 
        tags=tags, url=f'http://192.168.1.121:8080/{value.filename}'
        ))

    clothes = (await Clothes.read(kwargs=dict(_id=clothes_id)))[0]
    
    return clothes


@router.put('/{_id}', status_code=204, response_class=Response)
async def update_clothes(_id: str, clothes: UpdateClothes):
    await Clothes.update(PyObjectId(_id), clothes)


@router.delete('/{_id}', status_code=204, response_class=Response)
async def delete_clothes(_id: str, wardrobe_id: Optional[str] = None):
    _id = PyObjectId(_id)

    if wardrobe_id:
        wardrobe_id = PyObjectId(wardrobe_id)

        wardrobe = (await Wardrobe.read(kwargs={"_id": wardrobe_id}))[0]
        clothes_on_database = await Clothes.read(
            kwargs={"$and": [{"_id": {"$in": wardrobe.clothes}}, {"_id": _id}]}
        )
        if not clothes_on_database:
            return HTTPException(status_code=404, detail="Clothes not found on wardrobe")

    await Clothes.delete(_id)
