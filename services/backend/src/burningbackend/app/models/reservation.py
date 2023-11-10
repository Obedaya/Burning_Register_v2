from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic.fields import Field
from pydantic import BaseModel


class Reservation(Document):
    timestamp: datetime
    movie: str
    seat_number: int
    email: str
    scanned: bool = False

    class Settings:
        name = "reservations"


class ScanReservation(BaseModel):
    scanned: bool = True
