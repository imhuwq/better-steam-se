FROM imhuwq/python35
MAINTAINER imhuwq "imhuwq@gmail.com"


RUN adduser deploy --gecos "" --disabled-password
RUN mkdir -p /data && \
    mkdir -p /data/repo && \
    mkdir -p /data/logs && \
    chown -R deploy:deploy /data && \
    chmod -R 775 /data

ADD $PWD /data/repo
WORKDIR /data/repo
RUN pip install -r requirements.txt

USER deploy
