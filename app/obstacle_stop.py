import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "192.168.137.94"
port = 1883  # default MQTT broker port

is_obstacle_present = False

client = mqtt.Client()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("alphabot2/sensors/obstacle/right")
    client.subscribe("alphabot2/sensors/obstacle/left")
    client.publish("alphabot2/actuators/move", "forward")


def on_message(client, userdata, msg):
    global is_obstacle_present

    right_obstacle = False
    left_obstacle = False

    if msg.topic == "alphabot2/sensors/obstacle/right":
        msg_str = msg.payload.decode()
        right_obstacle = True if msg_str == "True" else False 
    elif msg.topic == "alphabot2/sensors/obstacle/left":
        msg_str = msg.payload.decode()
        left_obstacle = True if msg_str == "True" else False 

    is_obstacle_present = (left_obstacle or right_obstacle)

    # Publish motor speeds
    msg = "forward"
    if is_obstacle_present:
        print("obstacle is present!")
        msg = "stop"
    else:
        print("obstacle cleared!")
    client.publish("alphabot2/actuators/move", msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

# Start the loop
client.loop_forever()
