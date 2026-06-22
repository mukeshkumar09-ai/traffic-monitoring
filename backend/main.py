from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, SessionLocal
from backend.models import (
    Base,
    Traffic,
    Violation
)

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Edge Smart Traffic Monitoring API",
    description="Vehicle Detection, Tracking and Counting System",
    version="1.0.0"
)
app.mount(
    "/evidence",
    StaticFiles(directory="evidence"),
    name="evidence"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Database Connected Successfully"
    }


@app.post("/traffic")
def add_traffic(count: int):

    db = SessionLocal()

    traffic = Traffic(
        vehicle_count=count
    )

    db.add(traffic)

    db.commit()

    db.refresh(traffic)

    db.close()

    return {
        "message": "Traffic record added",
        "count": count
    }


from typing import Optional

@app.get("/history")
def get_history(camera_id: Optional[str] = None):

    db = SessionLocal()

    query = db.query(Traffic)

    if camera_id and camera_id != "ALL":
        query = query.filter(
            Traffic.camera_id == camera_id
        )

    records = query.all()

    result = []

    for row in records:
        result.append({
            "id": row.id,
            "camera_id": row.camera_id,
            "vehicle_count": row.vehicle_count,
            "timestamp": row.timestamp
        })

    db.close()

    return result


@app.get("/latest")
def latest_count():

    db = SessionLocal()

    latest = (
        db.query(Traffic)
        .order_by(Traffic.id.desc())
        .first()
    )

    db.close()

    if latest is None:
        return {
            "message": "No data found"
        }

    return {
        "vehicle_count": latest.vehicle_count,
        "timestamp": latest.timestamp
    }


    if vehicle_count < 20:
       status = "🟢 Low"

    elif vehicle_count < 50:
       status = "🟡 Moderate"

    else:
      status = "🔴 Heavy"

    db = SessionLocal()

    latest = (
        db.query(Traffic)
        .order_by(Traffic.id.desc())
        .first()
    )

    db.close()

    if latest is None:
        return {
            "message": "No data found"
        }

    vehicle_count = latest.vehicle_count

    if vehicle_count < 20:
        status = "Low"
    elif vehicle_count < 50:
        status = "Moderate"
    else:
        status = "Heavy"

    return {
        "vehicle_count": vehicle_count,
        "traffic_status": status
    }
@app.get("/status")
def traffic_status():

    db = SessionLocal()

    latest = (
        db.query(Traffic)
        .order_by(Traffic.id.desc())
        .first()
    )

    db.close()

    if latest is None:
        return {
            "message": "No data found"
        }

    vehicle_count = latest.vehicle_count

    if vehicle_count < 20:
        status = "🟢 Low"
    elif vehicle_count < 50:
        status = "🟡 Moderate"
    else:
        status = "🔴 Heavy"

    return {
        "vehicle_count": vehicle_count,
        "traffic_status": status
    }
@app.get("/analytics")
def analytics(camera_id: Optional[str] = None):

    db = SessionLocal()

    query = db.query(Traffic)

    if camera_id and camera_id != "ALL":
        query = query.filter(
            Traffic.camera_id == camera_id
        )

    records = query.all()

    db.close()

    if len(records) == 0:
        return {
            "peak_traffic": 0,
            "average_traffic": 0,
            "total_records": 0
        }

    counts = [
        r.vehicle_count
        for r in records
    ]

    peak_traffic = max(counts)

    average_traffic = round(
        sum(counts) / len(counts),
        2
    )

    total_records = len(records)

    return {
        "peak_traffic": peak_traffic,
        "average_traffic": average_traffic,
        "total_records": total_records
    }


@app.get("/peak-hour")
def peak_hour():

    db = SessionLocal()

    records = db.query(Traffic).all()

    db.close()

    if not records:
        return {
            "peak_hour": "No Data"
        }

    hour_counts = {}

    for record in records:

        hour = record.timestamp.hour

        if hour not in hour_counts:
            hour_counts[hour] = []

        hour_counts[hour].append(
            record.vehicle_count
        )

    peak_hour = max(
        hour_counts,
        key=lambda h: sum(hour_counts[h]) /
        len(hour_counts[h])
    )

    return {
        "peak_hour": f"{peak_hour}:00 - {peak_hour+1}:00"
    }
@app.get("/trend")
def traffic_trend():

    db = SessionLocal()

    records = (
        db.query(Traffic)
        .order_by(Traffic.id.desc())
        .limit(10)
        .all()
    )

    db.close()

    if len(records) < 10:
        return {
            "trend": "Insufficient Data"
        }

    records.reverse()

    first_half = records[:5]
    second_half = records[5:]

    avg_first = sum(
        r.vehicle_count for r in first_half
    ) / 5

    avg_second = sum(
        r.vehicle_count for r in second_half
    ) / 5

    if avg_second > avg_first:
        trend = "📈 Increasing"
    else:
        trend = "📉 Decreasing"

    return {
        "trend": trend
    }
@app.get("/cameras")
def get_cameras():

    db = SessionLocal()

    cameras = (
        db.query(Traffic.camera_id)
        .distinct()
        .all()
    )

    db.close()

    return [camera[0] for camera in cameras]


@app.get("/camera/{camera_id}")
def get_camera_data(camera_id: str):

    db = SessionLocal()

    records = (
        db.query(Traffic)
        .filter(Traffic.camera_id == camera_id)
        .all()
    )

    db.close()

    result = []

    for row in records:
        result.append({
            "id": row.id,
            "camera_id": row.camera_id,
            "vehicle_count": row.vehicle_count,
            "timestamp": row.timestamp
        })

    return result
# ==========================
# GET ALL VIOLATIONS
# ==========================

@app.get("/violations")
def get_violations():

    db = SessionLocal()

    violations = (
        db.query(Violation)
        .order_by(
            Violation.id.desc()
        )
        .all()
    )

    db.close()

    result = []

    for row in violations:

        result.append({
            "id": row.id,
            "camera_id": row.camera_id,
            "violation_type": row.violation_type,
            "image_path": row.image_path,
            "timestamp": row.timestamp
        })

    return result
# ==========================
# ADD TEST VIOLATION
# ==========================

@app.post("/add-violation")
def add_violation():

    db = SessionLocal()

    violation = Violation(
        camera_id="CAM01",
        violation_type="No Helmet",
        image_path="vehicle_35.jpg"
    )

    db.add(violation)

    db.commit()

    db.refresh(violation)

    db.close()

    return {
        "message": "Violation Added"
    }