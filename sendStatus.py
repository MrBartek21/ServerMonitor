import paho.mqtt.client as mqtt
import time, os
import socket


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")



broker = str(os.getenv('MQTT_BROKER', "192.168.1.4"))
port = int(os.getenv('MQTT_PORT', 1883))
topic_name = str(os.getenv('MQTT_TOPIC', "monitor"))
node_name = str(os.getenv('NODE_NAME', "nodename"))


client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker, port, 60)

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

topic_cpu = topic_name+'/'+node_name+'/cpuTemp'
topic_hostname = topic_name+'/'+node_name+'/hostname'
topic_localip= topic_name+'/'+node_name+'/localip'


while True:
  try:
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    tempC = temp/1000

    client.publish(topic_cpu, payload=tempC, qos=0, retain=False)
    client.publish(topic_localip, payload=local_ip, qos=0, retain=False)
    client.publish(topic_hostname, payload=hostname, qos=0, retain=False)


    print(f"send {tempC} to {topic_cpu}")
    print(f"send {local_ip} to {topic_localip}")
    print(f"send {hostname} to {topic_hostname}")

    time.sleep(20)
  except:
    tFile.close()
    client.loop_forever()