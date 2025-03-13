import zmq
import threading

context = zmq.Context()
# Publisher to forward data to hexapod
hexapod_socket = context.socket(zmq.PUB)
hexapod_socket.bind("tcp://*:5558")  # New port for hexapod

# Function to receive data from object detection (port 5555)
def receive_from_object_detection():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    sender_socket = context.socket(zmq.PUB)
    sender_socket.bind("tcp://*:5557")  # This will forward data to extra sender

    while True:
        data = socket.recv_json()
        print("[Object Detection] Received:", data)

        # Forward data to extra sender
        sender_socket.send_json(data)
        print("[Receiver] Forwarded to dummy_ai")

# Function to receive data from extra sender (port 5556)
def receive_from_dummy_ai():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        data = socket.recv_json()
        print("[dummy_ai] Received:", data)
        hexapod_socket.send_json(data)
        print("[dummy_ai] Forwarded to Hexapod")
        
# Start both receiver threads
thread1 = threading.Thread(target=receive_from_object_detection, daemon=True)
thread2 = threading.Thread(target=receive_from_dummy_ai, daemon=True)

thread1.start()
thread2.start()

# Keep the main program running
thread1.join()
thread2.join()
