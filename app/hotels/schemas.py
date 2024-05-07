from pydantic import BaseModel, ConfigDict


class Hotel(BaseModel):
    """Модель отображения отеля."""
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class HotelDetailed(Hotel):
    """Модель отображения отеля с количеством доступных номеров."""
    rooms_left: int
