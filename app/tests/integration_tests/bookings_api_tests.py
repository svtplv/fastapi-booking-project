from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    *[(1, '2030-05-01', '2030-05-05', 200)] * 5,
    (1, '2030-05-01', '2030-05-05', 409)
])
async def test_add_and_get_booking(room_id, date_from, date_to,
                                   status_code, auth_client: AsyncClient):
    response = await auth_client.post('/bookings', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to
    })

    assert response.status_code == status_code
