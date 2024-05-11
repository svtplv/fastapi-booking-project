from typing import TYPE_CHECKING, Any, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.hotels.rooms.models import Rooms


class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[dict[str, Any]]
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms: Mapped[List['Rooms']] = relationship(back_populates='hotel')

    def __str__(self):
        return f'<Отель: {self.name}>'
