from datetime import date
from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.schemas import Booking
from app.bookings.service import BookingService
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.exceptions import RoomNotAvailableException
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
async def get_bookings(
    user: Users = Depends(get_current_user)
) -> list[Booking]:
    return await BookingService.get_all(user_id=user.id)


@router.get('/{id}')
async def get_booking(id: int):
    return await BookingService.get_by_id(id)


@router.post('')
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    booking_dict = parse_obj_as(Booking, booking).dict()
    send_booking_confirmation_email.delay(
        booking_dict, user.email
    )
    if not booking_dict:
        raise RoomNotAvailableException
    return booking_dict


@router.delete('/{booking_id}')
async def delete_booking(
    booking_id: int, user: Users = Depends(get_current_user)
):
    result = await BookingService.delete(
        id=booking_id, user_id=user.id
    )
    return result
