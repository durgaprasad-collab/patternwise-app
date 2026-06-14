from datetime import date
from datetime import time
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class BirthProfile(Base):
    __tablename__ = "birth_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    birth_date: Mapped[date] = mapped_column(Date)

    birth_time: Mapped[time] = mapped_column(Time)

    location_name: Mapped[str] = mapped_column(
        String(255)
    )

    latitude: Mapped[float] = mapped_column(Float)

    longitude: Mapped[float] = mapped_column(Float)

    timezone: Mapped[str] = mapped_column(
        String(100)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    user = relationship(
        "User",
        back_populates="birth_profiles"
    )

    chart_calculations = relationship(
        "ChartCalculation",
        back_populates="birth_profile"
    )

    