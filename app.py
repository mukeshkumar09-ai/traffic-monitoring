from ultralytics import YOLO
import cv2

# Load YOLO Model
model = YOLO("yolov8n.pt")

# Open Video
cap = cv2.VideoCapture("videos/traffic.mp4")

# Counting Line Position
line_y = 800

# Vehicle Classes to Count
vehicle_classes = ["car", "bus", "truck", "motorcycle"]

# Store counted IDs
counted_ids = set()

# Total Vehicle Count
vehicle_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Tracking
    results = model.track(
        frame,
        persist=True,
        conf=0.5
    )

    annotated = results[0].plot()

    # Draw Counting Line
    cv2.line(
        annotated,
        (0, line_y),
        (annotated.shape[1], line_y),
        (0, 255, 0),
        3
    )

    # Check detections
    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        for box, track_id, cls_id in zip(boxes, ids, classes):

            class_name = model.names[int(cls_id)]

            # Count only vehicles
            if class_name not in vehicle_classes:
                continue

            x1, y1, x2, y2 = map(int, box)

            center_y = (y1 + y2) // 2

            track_id = int(track_id)
            print(f"ID:{track_id} CenterY:{center_y}")

            # Vehicle crosses line
            if abs(center_y - line_y) < 100:

                if track_id not in counted_ids:

                    counted_ids.add(track_id)
                    vehicle_count += 1

                    print(
                        f"Vehicle Count = {vehicle_count} | "
                        f"ID = {track_id} | "
                        f"Type = {class_name}"
                    )

    # Display Count
    cv2.putText(
        annotated,
        f"Vehicle Count: {vehicle_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.imshow("Smart Traffic Monitoring", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()