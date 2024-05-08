from datetime import date

import pytest

from app.hotels.service import HotelService


@pytest.mark.parametrize('location, date_from, date_to', [
    ('Алтай', date(2100, 1, 1), date(2100, 1, 2)),
    pytest.param(
        'Алтай', date(2200, 1, 1), date(2100, 1, 2), marks=pytest.mark.xfail
    ),
    pytest.param(
        'Алтай', date(2000, 1, 1), date(2000, 1, 2), marks=pytest.mark.xfail
    ),
])
async def test_get_hotels(location, date_from, date_to):
    hotels = await HotelService.get_hotels_by_location_and_time(
        location, date_from, date_to
    )

    assert hotels
