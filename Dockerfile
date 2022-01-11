FROM python:3

LABEL "Author"="MrBartek21"
LABEL version="1.2"


COPY ./requirements.txt ./

RUN apt-get update
RUN apt-get install -y python-dev
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install paho-mqtt
RUN git clone https://github.com/eclipse/paho.mqtt.python
RUN cd paho.mqtt.python
RUN python3 paho.mqtt.python/setup.py install; exit 0


WORKDIR /app
COPY ./sendStatus.py ./

ENV MQTT_BROKER=192.168.1.4
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=monitor

CMD ["python3", "./sendStatus.py"]