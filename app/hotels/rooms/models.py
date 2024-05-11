from typing import TYPE_CHECKING, Any, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.hotels.models import Hotels
    from app.bookings.models import Bookings


class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    services: Mapped[dict[str, Any]]
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped['Hotels'] = relationship(back_populates='rooms')
    bookings: Mapped[List['Bookings']] = relationship(back_populates='room')

    def __str__(self):
        return f'<Room - {self.name}>'
