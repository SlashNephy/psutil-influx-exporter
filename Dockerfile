FROM python:3.8-alpine

RUN apk add --update --no-cache --virtual .build-deps \
        build-base \
        linux-headers \
    && pip install --no-cache-dir \
        psutil \
        aiohttp \
    && apk del --purge .build-deps

COPY entrypoint.py /entrypoint.py
WORKDIR /

ENV INTERVAL=30
ENV INFLUX_ADDR=http://influxdb:8086
ENV INFLUX_DB=psutil

ENTRYPOINT ["python", "-u", "/entrypoint.py"]
