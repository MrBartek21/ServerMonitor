# INSTALATION
docker pull 192.168.1.115:5000/server_monitor-arm64:<version>

# RUN COMMAND
docker run -d 192.168.1.115:5000/server_monitor-arm64:<version>

# ENV Variable
MQTT_BROKER=192.168.1.4
MQTT_PORT=1883
MQTT_TOPIC=monitor
HOST_HOSTNAME=hostname