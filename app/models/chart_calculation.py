from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class ChartCalculation(Base):
    __tablename__ = "chart_calculations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("birth_profiles.id")
    )
    
    profile_json = mapped_column(
    JSON,
    nullable=True
    )
    chart_system: Mapped[str] = mapped_column(
        String(50)
    )

    ayanamsa: Mapped[str] = mapped_column(
        String(50)
    )

    chart_json: Mapped[dict] = mapped_column(
        JSON
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    version: Mapped[int] = mapped_column(
    default=1,
    nullable=False,
    server_default="1"
    )

    birth_profile = relationship(
        "BirthProfile",
        back_populates="chart_calculations"
    )
    __table_args__ = (
    UniqueConstraint(
        "profile_id",
        "chart_system",
        name="uq_profile_chart_system"
    ),
)