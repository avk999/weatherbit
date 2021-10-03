FROM python:3

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /

CMD ["/usr/local/bin/python", "weatherbit-mqtt.py"]