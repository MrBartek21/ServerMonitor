import subprocess
import paho.mqtt.client as mqtt
import time, os
import socket



def uptime1():
    raw = subprocess.check_output('uptime').decode("utf8").replace(',', '')
    days = int(raw.split()[2])
    if 'min' in raw:
        hours = 0
        minutes = int(raw[4])
    else:
        hours, minutes = map(int,raw.split()[4].split(':'))
    #print(days, hours, minutes)    
    totalsecs = ((days * 24 + hours) * 60 + minutes) * 60
    return totalsecs


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")



broker = str(os.getenv('MQTT_BROKER', "192.168.1.4"))
port = int(os.getenv('MQTT_PORT', 1883))
topic_name = str(os.getenv('MQTT_TOPIC', "monitor"))


client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker, port, 60)

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

topic_cpu = topic_name+'/'+hostname+'/cpuTemp'
topic_uptime = topic_name+'/'+hostname+'/uptime'
topic_localip= topic_name+'/'+hostname+'/localip'

while True:
  try:
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    tempC = temp/1000
    uptime = uptime1()

    client.publish(topic_cpu, payload=tempC, qos=0, retain=False)
    client.publish(topic_uptime, payload=uptime, qos=0, retain=False)
    client.publish(topic_localip, payload=local_ip, qos=0, retain=False)

    print(f"send {tempC} to {topic_cpu}")
    print(f"send {uptime} to {topic_uptime}")
    print(f"send {local_ip} to {topic_localip}")
    time.sleep(10)

  except:
    tFile.close()
    client.loop_forever()