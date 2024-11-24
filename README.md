# Butler
-Object/Color Detectuin
-Grid Setup
-Returning State Vectors

# Training and Setup
Install Dependencies:
pip install torch torchvision
pip install opencv-python
pip install matplotlib
pip install pyyaml
pip install torch torchvision opencv-python

1. Environment Setup

git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt

2. Create data.yaml

path: ../data/soccer   # path to your dataset folder
train: images/train
val: images/val

nc: 4  # number of classes (ball, robot, goal, boundary)
names: ['ball', 'robot', 'goal', 'boundary']

3. Optimizing 
python export.py --weights runs/train/soccer_model/weights/best.pt --include tflite

4. Folder Structure
dataset/
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   ├── labels/
│   │   ├── image1.txt
│   │   └── image2.txt
├── val/
│   ├── images/
│   └── labels/

5. Training
python train.py --img 640 --batch 16 --epochs 50 --data data.yaml --weights yolov5s.pt


6. Test
python detect.py --weights runs/train/ball_model/weights/best.pt --img 640 --source image.jpg


# Running # 

1. pip install torch torchvision opencv-python

2. git clone https://github.com/ultralytics/yolov5.git
   cd yolov5

3. 

import cv2
import torch

# Load the trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp/weights/best.pt')

# Open DroidCam stream (replace with 1 for USB or the URL for Wi-Fi)
cap = cv2.VideoCapture(1)  # or use url = "http://<ip_address>:4747/video" for Wi-Fi

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Render results on the frame
    frame = results.render()[0]

    # Display the frame with detection
    cv2.imshow('YOLOv5 Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
