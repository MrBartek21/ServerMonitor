FROM python:latest as builder

COPY ./requirements.txt ./

RUN apt-get update \
 && apt-get install -y \
        swig \
        python-dev \
        libssl-dev \
 && rm -rf /var/lib/apt/lists/*

 
#RUN apt update
#RUN apt install -y --no-install-recommends gcc make build-essential scons swig
RUN pip3 install --user -r requirements.txt
RUN git clone https://github.com/eclipse/paho.mqtt.python
RUN cd paho.mqtt.python
RUN python3 setup.py install

# Executor
FROM python:latest
 
WORKDIR /app
 
COPY --from=builder /root/.local /root/.local
COPY ./sendStatus.py ./

ENV Broker=192.168.1.4
ENV Port=1883
ENV Topic=monitor

CMD ["python3", "./sendStatus.py"]
