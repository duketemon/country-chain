FROM python:3.7
LABEL maintainer "Artem Kuchumov <duketemon@gmail.com>"

WORKDIR /lib
RUN wget http://download.redis.io/redis-stable.tar.gz &&\
    tar xvzf redis-stable.tar.gz
WORKDIR /lib/redis-stable
RUN make && make install &&\
    rm /lib/redis-stable.tar.gz

ENV REDIS_PORT=6379\
    REDIS_CONFIG_FILE=/etc/redis/6379.conf\
    REDIS_LOG_FILE=/var/log/redis_6379.log\
    REDIS_DATA_DIR=/var/lib/redis/6379\
    REDIS_EXECUTABLE=/usr/local/bin/redis-server
RUN utils/install_server.sh

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

ENV TELEGRAM_BOT_TOKEN INSERT_TELEGRAM_BOT_TOKEN_HERE
WORKDIR /usr/src/app/source
CMD /usr/local/bin/redis-server --daemonize yes &&\
    python app.py
