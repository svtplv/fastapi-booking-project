from datetime import date

from sqlalchemy import func, select

from app.bookings.service import get_all_booked_rooms_cte
from app.database import async_session_maker
from app.exceptions import NegativeTimeDeltaException
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class RoomService(BaseService):
    model = Rooms

    @classmethod
    async def get_all_by_hotel_and_time(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        if date_from > date_to:
            raise NegativeTimeDeltaException
        booked_rooms = get_all_booked_rooms_cte(
            date_from=date_from,
            date_to=date_to
        )
        hotel_rooms = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label('total_cost'),
                (Rooms.quantity - func.coalesce(
                    booked_rooms.c.booked_rooms_total, 0)).label('rooms_left'),
            )
            .join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            )
            .where(Rooms.hotel_id == hotel_id)
        )
        async with async_session_maker() as session:
            rooms = await session.execute(hotel_rooms)
            return rooms.mappings().all()
