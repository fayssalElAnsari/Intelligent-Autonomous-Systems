import numpy as np
import paho.mqtt.client as mqtt

broker_address = "192.168.137.94"  # MQTT broker address
port = 1883  # Default MQTT port

# Initialize a simple weight matrix
weight_matrix = np.array([[100, -100], [-100, 100]])

# Convert obstacle data to numerical format
def obstacle_to_numeric(obstacle):
    return 1.0 if obstacle == "true" else -1.0

# Process obstacle data and compute motor speeds
def process_data(left_obstacle, right_obstacle):
    inputs = np.array([obstacle_to_numeric(left_obstacle), obstacle_to_numeric(right_obstacle)])
    speeds = np.dot(weight_matrix, inputs)
    return np.clip(speeds, -200, 200)  # Clip speeds to the range [-200, 200]

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("alphabot2/sensors/obstacle/right")
    client.subscribe("alphabot2/sensors/obstacle/left")

left_obstacle = False
right_obstacle = False

def on_message(client, userdata, msg):
    global left_obstacle, right_obstacle

    if msg.topic == "alphabot2/sensors/obstacle/right":
        right_obstacle = msg.payload.decode()
    elif msg.topic == "alphabot2/sensors/obstacle/left":
        left_obstacle = msg.payload.decode()

    # Process the obstacle data
    left_speed, right_speed = process_data(left_obstacle, right_obstacle)

    # Publish motor speeds
    motor_speed_command = f"{left_speed} {right_speed}"
    print(motor_speed_command)
    client.publish("alphabot2/actuators/motors", motor_speed_command)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

# Start the loop
client.loop_forever()
