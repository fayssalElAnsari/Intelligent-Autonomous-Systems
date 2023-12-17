# Autonomous Alphabot 2 Program

In this program we try to implement a system capable of controlling the alphabot. 

The code provided allows us to deploy an MQTT server capable of reporting the sensor values of the IRsensors and publishing them on a seperate topic. Will also allow us to controll the alphabot by publishing to the motors topics.

## TODO

### 1st algorithm: Stop On Obstacle
* **obstacle detection** : network
* **movement commands** : network

In the first program we try to create a controller for the alphabot2 that makes it stop whenever an obstacle is in front of it.

One way to do this is to take in the values published on the sensors topics. And send the respective `forward` or 'stop' commands. We need to make sure that if the obstacle is no longer in fron of the robot it will automatically continue moving. Also we need to make sure that the response time is proportional to the speed in order to get a safe stopping distance, meaning the robot shouldn't touch the obstacles in fron of it.
The problem with this implementation is that using the sensor values published instead of taking the values directly from the alphabot adds a latency. So an improvement would be to controll the alphabot directly without usnig the MQTT servers, for either the sensors values the motor controlss or both. Depending on the outcomes of the tests.

#### Results
As expected the tests show that with the default forward speed the robot hits the obstacle.
Default speed: 30.
Maximum possible speed: 10.

### 2nd algorithm: avoid white lines (or follow white lines)



