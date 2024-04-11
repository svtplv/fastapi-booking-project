from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.bookings.router import router as router_bookings
from app.config import settings
from app.users.router import router as router_users
from app.hotels.rooms.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )
    FastAPICache.init(RedisBackend(redis), prefix='cache')
