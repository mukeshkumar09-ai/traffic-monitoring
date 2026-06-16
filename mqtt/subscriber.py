import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import json
import paho.mqtt.client as mqtt

from backend.database import SessionLocal
from backend.models import Traffic

broker = "broker.hivemq.com"
port = 1883
topic = "traffic-monitoring/mukesh2025"


def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)

    result, mid = client.subscribe(topic)

    print("Subscribed to:", topic)
    print("Subscribe Result:", result)


def on_message(client, userdata, msg):
    print("RAW:", msg.payload.decode())

    payload = json.loads(
        msg.payload.decode()
    )

    count = payload["vehicle_count"]

    db = SessionLocal()

    traffic = Traffic(
        vehicle_count=count
    )

    db.add(traffic)

    db.commit()

    db.close()

    print(
        f"Stored Count: {count}"
    )


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    broker,
    port,
    60
)

print("Listening...")

client.loop_forever()