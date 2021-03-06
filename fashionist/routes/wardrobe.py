from fastapi import APIRouter, Response, HTTPException

from ..models import PyObjectId
from ..models.wardrobe import Wardrobe, UpdateWardrobe

router = APIRouter(prefix='/wardrobes')


@router.get('/{_id}', status_code=200, response_model=Wardrobe)
async def get_wardrobe(
        _id: str,
        outfits_offset: int = 0,
        outfits_limit: int = 10,
        clothes_offset: int = 0,
        clothes_limit: int = 10
):
    wardrobe = await Wardrobe.read_extra(
        query={"_id": PyObjectId(_id)},
        extra={
            "outfits": {
                "$slice": [outfits_offset, outfits_limit]
            },
            "clothes": {
                "$slice": [clothes_offset, clothes_limit]
            }
        })

    if not wardrobe:
        raise HTTPException(status_code=404, detail="Wardrobe not found")

    return wardrobe[0]


@router.post('/', status_code=201, response_model=Wardrobe)
async def create_wardrobe(wardrobe: Wardrobe):
    await Wardrobe.create(wardrobe)
    return wardrobe


@router.put('/{_id}', status_code=204, response_class=Response)
async def update_wardrobe(_id: str, wardrobe: UpdateWardrobe):
    await Wardrobe.update(PyObjectId(_id), wardrobe)


@router.delete('/{_id}', status_code=204, response_class=Response)
async def delete_wardrobe(_id: str):
    await Wardrobe.delete(PyObjectId(_id))
