FROM phusion/baseimage

RUN apt-get update -q && \
    apt-get install wget && \
    apt-get install -y vim git build-essential supervisor && \
    apt-get install -y libffi-dev libpq-dev libjpeg-dev && \
    apt-get install -y python-dev python-setuptools python-apt python-pip && \
    pip install --upgrade pip && \
    pip install python-intercom>=2.1.1 \
                tornado==4.4.1 \
                html2text==2016.9.19 \
                indicoio==0.16.3

ADD . /intercombot
WORKDIR /intercombot

RUN python setup.py develop

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
