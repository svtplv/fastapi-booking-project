from pydantic import BaseModel


class Room(BaseModel):
    """Модель отображения номера."""
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int

    class Config:
        from_attributes = True


class RoomDetailed(Room):
    """
    Модель отображения номера с количеством оставшихся комнат и полной ценой.
    """
    total_cost: int
    rooms_left: int
