# Butler
-Object/Color Detectuin
-Grid Setup
-Returning State Vectors


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


