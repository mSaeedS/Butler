import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

def receive_data():
    while True:
        data = socket.recv_json()
        print("Received data:", data)
        # Process or forward data as needed

receive_data()