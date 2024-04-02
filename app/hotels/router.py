from datetime import date

from fastapi import APIRouter

from app.exceptions import HotelsNotAvailableException
from app.hotels.service import HotelService
from app.hotels.schemas import Hotel, HotelDetailed


router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.get('/{location}')
async def get_available_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> list[HotelDetailed]:
    """Возвращает доступные для брони отели по заданным параметрам."""

    hotels = await HotelService.get_hotels_by_location_and_time(
        location=location,
        date_from=date_from,
        date_to=date_to
    )
    if not hotels:
        raise HotelsNotAvailableException
    return hotels


@router.get('/id/{hotel_id}')
async def get_hotel_by_id(
    hotel_id: int,
) -> Hotel | None:
    return await HotelService.get_one_or_none(id=hotel_id)
