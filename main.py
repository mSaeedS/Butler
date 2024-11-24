import torch
import cv2

# Load the model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

# Load video or image
cap = cv2.VideoCapture(0)  # Or use path to your video or stream URL

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame)

    # Render results
    frame = results.render()[0]

    # Show the frame
    cv2.imshow('YOLOv5 Inference', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
