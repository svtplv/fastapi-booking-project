from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('email, password, status_code', [
    ('third@gmail.com', 'testpass', 200),
    ('first@test.com', 'already_registered', 409),
    ('test', 'testpass', 422),
])
async def test_register_user(email, password,
                             status_code, client: AsyncClient):
    response = await client.post('/auth/register', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('first@test.com', 'first_pass', 200),
    ('second@test.com', 'second_pass', 200),
    ('nonexistant@example.com', 'password', 401),
    ('first@test.com', 'incorrect_password', 401),
])
async def test_login_user(email, password, status_code, client: AsyncClient):
    response = await client.post('/auth/login', json={
        'email': email,
        'password': password,
    })
    assert response.status_code == status_code
