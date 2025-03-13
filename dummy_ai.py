import zmq
import random
import time
import threading

context = zmq.Context()




# Function to send random data (like before)
def send_random_data():
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")  # This remains unchanged

    while True:
        data = {
            "source": "dummy_ai",
            "action": (random.randint(0, 640), random.randint(0, 480)),
        }
        socket.send_json(data)
        print("[dummy_ai] Sent random data:", data)
        time.sleep(1)

# Function to receive forwarded data from receiver (port 5557)
def receive_from_receiver():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5557")
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        data = socket.recv_json()
        print("[dummy_ai] Received forwarded data:", data)
        
# Run both functions in separate threads
thread1 = threading.Thread(target=send_random_data, daemon=True)
thread2 = threading.Thread(target=receive_from_receiver, daemon=True)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
