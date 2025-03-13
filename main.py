import torch
import cv2
import zmq
import json
import time
# Load the model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'custom', path='latest.pt')

xd = []
input_active = True  # Flag to control mouse input

# Function to handle mouse clicks
def get_coordinates(event, x, y, flags, param):
    global input_active
    if event == cv2.EVENT_LBUTTONDOWN and input_active:  # Left mouse button clicked and input is active
        xd.append((x, y))
        print(f"Pixel coordinates: x={x}, y={y}")

# Load video or image
cap = cv2.VideoCapture(0)  # Or use path to your video or stream URL

# Create a named window for the YOLOv5 output and set the mouse callback
cv2.namedWindow("YOLOv5 Inference")
cv2.setMouseCallback("YOLOv5 Inference", get_coordinates)

# Sender Side (in your current script)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

def send_data(ball=None, hexapod=None, goal=None, coordinates=None):
    data = {
        'ball': ball,
        'hexapod': hexapod,
        'goal': goal,
        'coordinates': coordinates or []
    }
    socket.send_json(data)

# Initialize variables
ball = None
hexapod = None
goal = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Inference
    results = model(frame)


    # Process midpoint
    for *xyxy, conf, cls in results.xyxy[0]:
        # Get class name
        class_name = model.names[int(cls)]

        # Only process if the class is in target_classes
        if class_name == 'ball':
            # Convert to integers
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Calculate midpoint
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            
            # Store ball coordinates
            ball = (x_midpoint, y_midpoint)
            

        if class_name == 'hexapod':
            # Convert to integers
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Calculate midpoint
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            
            # Store hexapod coordinates
            hexapod = (x_midpoint, y_midpoint)

        if class_name == 'goal':
            # Convert to integers
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Calculate midpoint
            x_midpoint = (x1 + x2) // 2
            y_midpoint = (y1 + y2) // 2
            
            # Store hexapod coordinates
            goal = (x_midpoint, y_midpoint)
        
    
    # Send data even if no objects detected
    send_data(ball, hexapod, goal, xd)
    #send_data(0,1,2,3)
    #time.sleep(1)
    # Render results
    frame = results.render()[0]

    # Show the frame with YOLOv5 inference
    cv2.imshow('YOLOv5 Inference', frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to quit
        break
    elif key == ord('s'):  # Press 's' to toggle mouse input
        input_active = not input_active
        status = "enabled" if input_active else "disabled"
        print(f"Mouse input {status}")

# Release the video capture and destroy the window
cap.release()
cv2.destroyAllWindows()

# Print the collected coordinates
print("Collected coordinates:", xd)