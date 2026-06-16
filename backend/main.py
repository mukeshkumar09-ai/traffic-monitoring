from fastapi import FastAPI

app = FastAPI()

vehicle_count = 35

@app.get("/")
def home():
    return {
        "message": "Edge Smart Traffic Monitoring API"
    }

@app.get("/count")
def get_count():
    return {
        "vehicle_count": vehicle_count
    }
@app.get("/status")
def traffic_status():

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