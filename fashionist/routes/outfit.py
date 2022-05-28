from typing import List, Optional

from fastapi import APIRouter, Response

from ..models.outfit import Outfit, UpdateOutfit

router = APIRouter(prefix='/wardrobe/{wardrobe_id}/outfits')


@router.get('/', status_code=200, response_model=List[Outfit])
async def get_all_wardrobe_outfit(
        wardrobe_id: str,
        tags: Optional[List[str]],
        offset: int,
        limit: int
):
    pass


@router.get('/{_id}', status_code=200, response_model=Outfit)
async def get_wardrobe_outfit(wardrobe_id: str, _id: str):
    pass


@router.post('/', status_code=201, response_model=Outfit)
async def create_wardrobe_outfit(wardrobe_id: str, outfit: Outfit):
    pass


@router.put('/{_id}', status_code=204, response_class=Response)
async def update_wardrobe_outfit(
        wardrobe_id: str,
        _id: str,
        outfit: UpdateOutfit
):
    pass


@router.delete('/{_id}', status_code=204, response_class=Response)
async def delete_wardrobe_outfit(wardrobe_id: str, _id: str):
    pass
