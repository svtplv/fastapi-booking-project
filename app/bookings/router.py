from fastapi import APIRouter, Depends

from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingService.get_all(user_id=user.id)
    # return await BookingService.get_all()


@router.get('/{id}')
async def get_booking(id: int):
    return await BookingService.get_by_id(id)
