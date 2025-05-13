import zmq
import threading
import math
import keyboard
context = zmq.Context()
# Publisher to forward data to hexapod
hexapod_socket = context.socket(zmq.PUB)
hexapod_socket.bind("tcp://*:5558")  # New port for hexapod

def to_polar(x1, y1, x2, y2):
        if None in [x1, y1, x2, y2]:
            return None, None  # Return None or a default value if any coordinate is None
        dx = x2 - x1
        dy = y2 - y1
        r = math.hypot(dx, dy)  # sqrt(dx^2 + dy^2)
        theta = math.atan2(dy, dx)  # atan2 handles quadrant automatically
        return r, theta  # Returning theta in radians

def StateVector(data):

    ball = data['ball']
    hexapod = data['hexapod']
    obstacle = data['obstacle']
    coordinates = data['coordinates']
    if ball is None:
        ball_x, ball_y = None, None  # Assign None to both variables
    else:
        ball_x, ball_y = ball

    if hexapod is None:
        hexapod_x, hexapod_y = None, None  # Assign None to both variables
    else:
        hexapod_x, hexapod_y = hexapod

    if obstacle is None:
        obstacle_x, obstacle_y = None, None  # Assign None to both variables
    else:
        obstacle_x, obstacle_y = obstacle
    topwall_x, topwall_y = coordinates[0]
    bottomwall_x, bottomwall_y = coordinates[1]
    leftwall_x, leftwall_y = coordinates[2]
    rightwall_x, rightwall_y = coordinates[3]
    goal_x, goal_y = coordinates[4]

    #ball_hexapod,ball_obstacle,ball_goal,ball_topwall,ball_bottomwall,ball_leftwall,ball_rightwall,
    #hexapod_obstacle,hexapod_goal,hexapod_topwall,hexapod_bottomwall,hexapod_leftwall,hexapod_rightwall,
    #obstacle_goal,obstacle_topwall,obstacle_bottomwall, obstacle_leftwall,obstacle_rightwall
    ball_hexapod_r, ball_hexapod_theta = to_polar(ball_x, ball_y, hexapod_x, hexapod_y)
    ball_obstacle_r, ball_obstacle_theta = to_polar(ball_x, ball_y, obstacle_x, obstacle_y)
    ball_goal_r, ball_goal_theta = to_polar(ball_x, ball_y, goal_x, goal_y)
    ball_topwall_r, ball_topwall_theta = to_polar(ball_x, ball_y, topwall_x, topwall_y)
    ball_bottomwall_r, ball_bottomwall_theta = to_polar(ball_x, ball_y, bottomwall_x, bottomwall_y)
    ball_leftwall_r, ball_leftwall_theta = to_polar(ball_x, ball_y, leftwall_x, leftwall_y)
    ball_rightwall_r, ball_rightwall_theta = to_polar(ball_x, ball_y, rightwall_x, rightwall_y)

    hexapod_obstacle_r, hexapod_obstacle_theta = to_polar(hexapod_x, hexapod_y, obstacle_x, obstacle_y)
    hexapod_goal_r, hexapod_goal_theta = to_polar(hexapod_x, hexapod_y, goal_x, goal_y)
    hexapod_topwall_r, hexapod_topwall_theta = to_polar(hexapod_x, hexapod_y, topwall_x, topwall_y)
    hexapod_bottomwall_r, hexapod_bottomwall_theta = to_polar(hexapod_x, hexapod_y, bottomwall_x, bottomwall_y)
    hexapod_leftwall_r, hexapod_leftwall_theta = to_polar(hexapod_x, hexapod_y, leftwall_x, leftwall_y)
    hexapod_rightwall_r, hexapod_rightwall_theta = to_polar(hexapod_x, hexapod_y, rightwall_x, rightwall_y)

    obstacle_goal_r, obstacle_goal_theta = to_polar(obstacle_x, obstacle_y, goal_x, goal_y)
    obstacle_topwall_r, obstacle_topwall_theta = to_polar(obstacle_x, obstacle_y, topwall_x, topwall_y)
    obstacle_bottomwall_r, obstacle_bottomwall_theta = to_polar(obstacle_x, obstacle_y, bottomwall_x, bottomwall_y)
    obstacle_leftwall_r, obstacle_leftwall_theta = to_polar(obstacle_x, obstacle_y, leftwall_x, leftwall_y)
    obstacle_rightwall_r, obstacle_rightwall_theta = to_polar(obstacle_x, obstacle_y, rightwall_x, rightwall_y)
    return [
        (ball_hexapod_r, ball_hexapod_theta),
        (ball_obstacle_r, ball_obstacle_theta),
        (ball_goal_r, ball_goal_theta),
        (ball_topwall_r, ball_topwall_theta),
        (ball_bottomwall_r, ball_bottomwall_theta),
        (ball_leftwall_r, ball_leftwall_theta),
        (ball_rightwall_r, ball_rightwall_theta),
        
        (hexapod_obstacle_r, hexapod_obstacle_theta),
        (hexapod_goal_r, hexapod_goal_theta),
        (hexapod_topwall_r, hexapod_topwall_theta),
        (hexapod_bottomwall_r, hexapod_bottomwall_theta),
        (hexapod_leftwall_r, hexapod_leftwall_theta),
        (hexapod_rightwall_r, hexapod_rightwall_theta),
        
        (obstacle_goal_r, obstacle_goal_theta),
        (obstacle_topwall_r, obstacle_topwall_theta),
        (obstacle_bottomwall_r, obstacle_bottomwall_theta),
        (obstacle_leftwall_r, obstacle_leftwall_theta),
        (obstacle_rightwall_r, obstacle_rightwall_theta),
    ]



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
        vector = StateVector(data)
        # Forward data to ai
        sender_socket.send_json(vector)
        print("Forwarded to dummy_ai",vector)

# Function to receive data from extra sender (port 5556)
def receive_from_dummy_ai():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        data = socket.recv_json()
        print("Received from ai: ", data)
        hexapod_socket.send_json(data)
        print("Forwarded to Hexapod", data)

# Function to listen for key press to stop the program
def listen_for_stop():
    while True:
        if keyboard.is_pressed('x'):  # If the 'x' key is pressed
            
            exit(0)  # Exit the program

# Start both receiver threads
thread1 = threading.Thread(target=receive_from_object_detection, daemon=True)
thread2 = threading.Thread(target=receive_from_dummy_ai, daemon=True)


thread1.start()
thread2.start()


# Keep the main program running
thread1.join()
thread2.join()

