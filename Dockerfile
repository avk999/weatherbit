FROM python:3.11.0-alpine

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /

CMD ["/usr/local/bin/python", "weatherbit-mqtt.py"]
