import zmq

context = zmq.Context()

# Subscribe to receiver's forwarded data (port 5558)
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5558")
socket.setsockopt(zmq.SUBSCRIBE, b'')

print("[Hexapod] Connected to receiver, waiting for data...")

while True:
    data = socket.recv_json()
    print("[Hexapod] Received Data:", data)

    # Process the data as needed
