from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


# ==========================
# Traffic Table
# ==========================

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


# ==========================
# Violations Table
# ==========================

class Violation(Base):
    __tablename__ = "violations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    camera_id = Column(
        String
    )

    violation_type = Column(
        String
    )

    image_path = Column(
        String
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )