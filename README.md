# INSTALATION
docker pull 192.168.1.115:5000/server_monitor-arm64:version

# RUN COMMAND
docker run -d 192.168.1.115:5000/server_monitor-arm64:version

# Version
v1, v1.2, v1.3


# ENV Variable
MQTT_BROKER=192.168.1.4

MQTT_PORT=1883

MQTT_TOPIC=monitor

NODE_NAME=nodename