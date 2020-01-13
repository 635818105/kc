FROM alpine:3.6

RUN echo -e "http://mirrors.aliyun.com/alpine/v3.6/main\nhttp://mirrors.aliyun.com/alpine/v3.6/community" > /etc/apk/repositories
ENV LANG en_US.UTF-8
RUN apk add -U tzdata \
    && cp -r -f /usr/share/zoneinfo/Hongkong /etc/localtime
RUN apk add --no-cache ca-certificates python3 bash openssh git openssl-dev uwsgi uwsgi-python3
RUN apk add --no-cache --virtual .build-deps python3-dev gcc musl-dev libffi-dev make \
        && pip3 install --no-cache-dir --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ \
                pymysql==0.8.1 \
                Flask==1.0.2 \
                Flask-RESTful==0.3.6 \
                Flask-Script==2.0.6 \
                Flask-SQLAlchemy==2.3.2 \
                Flask-WTF==0.14.2 \
                Flask-Caching==1.6.0\
                SQLAlchemy==1.2.7 \
                celery==4.2.0 \
                requests==2.18.1 \
                pypinyin==0.35.1 \
                simplejson==3.16.0 \
                six==1.11.0 \
                xlrd==1.1.0 \
                xlwt==1.3.0 \
                msgpack==0.5.0 \
                pillow==5.4.1 \
                       && apk del .build-deps

RUN git clone https://github.com/Supervisor/supervisor.git \
        && cd supervisor \
        && python3 setup.py install \
        && cd .. \
        && rm -rf supervisor \
        && cd /etc/ \
        && echo_supervisord_conf > supervisord.conf \
        && echo '[include]' >> supervisord.conf \
        && echo 'files = /code/supervisor/*.ini' >> supervisord.conf \
        && supervisord -c /etc/supervisord.conf