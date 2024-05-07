from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.models import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.users.router import router as router_users
from app.hotels.rooms.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    yield

app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
