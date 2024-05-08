import pytest
from httpx import ASGITransport, AsyncClient

from app.config import settings
from app.database import Base, engine
from app.main import app as fastapi_app
from app.tests.utils import import_test_data


@pytest.fixture(scope='session', autouse=True)
async def setup_database():
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await import_test_data()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url='http://test'
    ) as client:
        yield client


@pytest.fixture(scope='session')
async def auth_client():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url='http://test'
    ) as client:

        await client.post('/auth/login', json={
            'email': 'first@test.com',
            'password': 'first_pass'
        })

        assert client.cookies['booking_access_token']
        yield client
