from datetime import date

import pytest

from app.bookings.service import BookingService


@pytest.mark.parametrize('user_id, room_id, date_from, date_to', [
    (1, 3, date(2100, 1, 1), date(2100, 1, 2)),
    pytest.param(
        1, 3, date(2200, 1, 1), date(2100, 1, 2), marks=pytest.mark.xfail
    ),
    pytest.param(
        1, 3, date(2000, 1, 1), date(2000, 1, 2), marks=pytest.mark.xfail
    ),
    pytest.param(
        1, 3, date(2100, 1, 1), date(2200, 1, 2), marks=pytest.mark.xfail
    ),
])
async def test_booking_crud(user_id, room_id, date_from, date_to):
    booking = await BookingService.add(user_id, room_id, date_from, date_to)

    assert booking.user_id == user_id
    assert booking.room_id == room_id

    booking = await BookingService.get_by_id(booking.id)

    assert booking

    await BookingService.delete(id=booking.id)

    deleted_booking = await BookingService.get_by_id(booking.id)

    assert not deleted_booking
