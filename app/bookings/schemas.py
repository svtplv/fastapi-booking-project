from datetime import date
from pydantic import BaseModel, ConfigDict


class Booking(BaseModel):
    """Модель отображения бронирования."""

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class BookingDetailed(Booking):
    """Модель отображения бронирования с подробностями о номере."""

    image_id: int
    name: str
    description: str
    services: list[str]
