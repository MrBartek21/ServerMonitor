# Preparation
sudo nano /etc/docker/daemon.json

{ "insecure-registries": ["192.168.1.115:5000"] }

 service docker restart

# INSTALATION
docker pull 192.168.1.115:5000/server_monitor:version

# RUN COMMAND
docker run -d --name Server_monitor -e NODE_NAME=service 192.168.1.115:5000/server_monitor:version

# Version
arm-v3
arm64-v3

arm-v4
arm64-v4

arm-v6
arm64-v6


# ENV Variable
MQTT_BROKER=192.168.1.4

MQTT_PORT=1883

MQTT_TOPIC=monitor

NODE_NAME=nodename