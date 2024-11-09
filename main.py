import cv2
import torch

# ESP32-CAM stream URL
stream_url = "http://192.168.18.103:81/stream"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use 'yolov5m', 'yolov5l', or 'yolov5x' for larger models

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection
    results = model(frame)

    # Render results on the frame
    results.render()

    # Display the frame with detections
    cv2.imshow("YOLOv5 Detection", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
