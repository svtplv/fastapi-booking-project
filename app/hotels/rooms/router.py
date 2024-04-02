from datetime import date

from app.hotels.rooms.service import RoomService
from app.hotels.rooms.schemas import RoomDetailed
from app.hotels.router import router


@router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[RoomDetailed]:
    """Возвращает сведения по номерам отелям за определенный период времени"""
    rooms = await RoomService.get_all_by_hotel_and_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
    return rooms
