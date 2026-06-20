import json
import random
import time

import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topic = "traffic-monitoring/mukesh2025"

CAMERA_ID = "CAM03"

client = mqtt.Client()

client.connect(
    broker,
    port,
    60
)

print(f"{CAMERA_ID} Publisher Connected")

while True:

    count = random.randint(20, 150)

    message = {
        "camera_id": CAMERA_ID,
        "vehicle_count": count
    }

    client.publish(
        topic,
        json.dumps(message)
    )

    print("Published:", message)

    time.sleep(5)