from datetime import date

from sqlalchemy import CTE, and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import (NegativeArivalException,
                            NegativeTimeDeltaException,
                            RoomNotAvailableException, StayLimitException)
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            if date_from > date_to:
                raise NegativeTimeDeltaException
            if date_from < date.today():
                raise NegativeArivalException
            if (date_to - date_from).days > 30:
                raise StayLimitException

            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id))
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            if not rooms_left:
                raise RoomNotAvailableException
            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price: int = price.scalar()
            new_booking = insert(Bookings).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price,
            ).returning(Bookings)

            new_booking = await session.execute(new_booking)
            await session.commit()
            return new_booking.scalar()


def get_all_booked_rooms_cte(date_from, date_to) -> CTE:
    booked_rooms = (
        select(Bookings.room_id, func.count(Bookings.room_id)
               .label('booked_rooms_total'))
        .select_from(Bookings)
        .where(
            or_(
                and_(
                    Bookings.date_from >= date_from,
                    Bookings.date_from <= date_to,
                ),
                and_(
                    Bookings.date_from <= date_from,
                    Bookings.date_to > date_from,
                ),
            ),
        )
        .group_by(Bookings.room_id)
        .cte('booked_rooms')
    )
    return booked_rooms
