from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, SessionLocal
from backend.models import Base, Traffic

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Edge Smart Traffic Monitoring API",
    description="Vehicle Detection, Tracking and Counting System",
    version="1.0.0"
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


@app.get("/history")
def get_history():

    db = SessionLocal()

    records = db.query(Traffic).all()

    result = []

    for row in records:
        result.append({
            "id": row.id,
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
def analytics():

    db = SessionLocal()

    records = db.query(Traffic).all()

    db.close()

    if len(records) == 0:
        return {
            "peak_traffic": 0,
            "average_traffic": 0,
            "total_records": 0
        }

    counts = [r.vehicle_count for r in records]

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
