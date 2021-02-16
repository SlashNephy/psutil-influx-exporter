# psutil-influx-exporter
A tiny tool to export psutil metrics

Demo -> [dashboard.starry.blue](https://dashboard.starry.blue/d/SwC1MrpWz/system?orgId=1&refresh=10s)

[![Docker Image Size (tag)](https://img.shields.io/docker/image-size/slashnephy/psutil-influx-exporter/latest)](https://hub.docker.com/r/slashnephy/psutil-influx-exporter)

`docker-compose.yml`

```yaml
version: '3.8'

services:
  influxdb:
    container_name: InfluxDB
    image: influxdb
    restart: always
    volumes:
      - influxdb:/var/lib/influxdb

  psutil-influx-exporter:
    container_name: psutil-influx-exporter
    image: slashnephy/psutil-influx-exporter:latest
    restart: always
    volumes:
      - /mnt:/mnt:ro
      - /:/ext/host:ro
    environment:
      # メトリックの取得間隔 (秒)
      INTERVAL: 10
      # InfluxDB アドレス
      INFLUX_ADDR: http://influxdb:8086
      # InfluxDB データベース名
      INFLUX_DB: psutil
      # マウントポイント
      MOUNT_POINTS: /mnt,/ext

volumes:
  influxdb:
    local: driver
```
