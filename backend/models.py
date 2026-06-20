from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    camera_id = Column(
        String,
        default="CAM01"
    )

    vehicle_count = Column(
        Integer
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )