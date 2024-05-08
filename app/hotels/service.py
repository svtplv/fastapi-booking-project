from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.service import get_all_booked_rooms_cte
from app.database import async_session_maker
from app.exceptions import NegativeArivalException, NegativeTimeDeltaException
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def get_hotels_by_location_and_time(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        if date_from > date_to:
            raise NegativeTimeDeltaException
        if date_from < date.today():
            raise NegativeArivalException
        booked_rooms = get_all_booked_rooms_cte(
            date_from=date_from,
            date_to=date_to
        )
        booked_hotels = (
            select(
                Rooms.hotel_id, func.sum(Rooms.quantity - func.coalesce(
                    booked_rooms.c.booked_rooms_total, 0
                )).label('rooms_left')
            )
            .select_from(Rooms)
            .join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            )
            .group_by(Rooms.hotel_id)
            .cte('booked_hotels')
        )
        available_hotels = (
            select(Hotels.__table__.columns, booked_hotels.c.rooms_left)
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id,
                  isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            rooms = await session.execute(available_hotels)
            return rooms.mappings().all()
