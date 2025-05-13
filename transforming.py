import torch
import torch.onnx
import yolov5  # Ensure yolov5 is installed via pip if needed

# Load your custom YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='latest.pt', force_reload=True)

# Set model to evaluation mode
model.eval()

# Define input size (use a smaller size like 320x320 for faster inference)
img_size = 320
dummy_input = torch.randn(1, 3, img_size, img_size)

# Export to ONNX
onnx_path = "latest.onnx"
torch.onnx.export(
    model,
    dummy_input,
    onnx_path,
    opset_version=12,
    input_names=['images'],
    output_names=['output'],
    dynamic_axes={'images': {0: 'batch'}, 'output': {0: 'batch'}}
)

print(f"Model exported to {onnx_path}")