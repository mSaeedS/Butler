import torch
import cv2
import zmq
import json
import time

# Check for GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the model and move to device
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
model.to(device)

xd = []
input_active = True  # Flag to control mouse input

# Mouse click handler
def get_coordinates(event, x, y, flags, param):
    global input_active
    if event == cv2.EVENT_LBUTTONDOWN and input_active:
        xd.append((x, y))
        print(f"Pixel coordinates: x={x}, y={y}")

# Load video
cap = cv2.VideoCapture(1)

cv2.namedWindow("YOLOv5 Inference")
cv2.setMouseCallback("YOLOv5 Inference", get_coordinates)

# ZMQ publisher
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

def send_data(ball=(0,0), hexapod=(2,2), obstacle=(0,2), coordinates=None):
    data = {
        'ball': ball,
        'hexapod': hexapod,
        'obstacle': obstacle,
        'coordinates': coordinates or []
    }
    socket.send_json(data)

ball = None
hexapod = None
obstacle = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Convert BGR to RGB BEFORE passing to model
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run inference (model handles resizing internally)
    results = model(rgb_frame, size=640)

    # Process detections
    for *xyxy, conf, cls in results.xyxy[0]:
        class_name = model.names[int(cls)]
        x1, y1, x2, y2 = map(int, xyxy)

        # Draw box + label directly using OpenCV (instead of results.render())
        color = (0, 255, 0)  # Default color (green)
        if class_name == 'ball':
            color = (0, 0, 255)  # Red
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            ball = (x_midpoint, y_midpoint)
        elif class_name == 'hexapod':
            color = (255, 0, 0)  # Blue
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            hexapod = (x_midpoint, y_midpoint)
        elif class_name == 'obstacle':
            color = (0, 255, 255)  # Yellow
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            obstacle = (x_midpoint, y_midpoint)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Send data even if no objects detected
    send_data(ball, hexapod, obstacle, xd)

    # Show annotated frame
    cv2.imshow('YOLOv5 Inference', frame)

    # Handle key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        input_active = not input_active
        status = "enabled" if input_active else "disabled"
        print(f"Mouse input {status}")

cap.release()
cv2.destroyAllWindows()

print("Collected coordinates:", xd)
