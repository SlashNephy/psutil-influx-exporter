# psutil-influx-exporter
A tiny tool to export psutil metrics

Supports InfluxDB 2.x.

`docker-compose.yml`

```yaml
version: '3.8'

services:
  influxdb:
    container_name: InfluxDB
    image: influxdb:2.3
    restart: always
    volumes:
      - influxdb:/var/lib/influxdb

  psutil-influx-exporter:
    container_name: psutil-influx-exporter
    image: ghcr.io/slashnephy/psutil-influx-exporter:master
    restart: always
    volumes:
      - /mnt:/mnt:ro
      - /:/ext/host:ro
    environment:
      # メトリックの取得間隔 (秒)
      INTERVAL: 10

      INFLUX_ADDR: http://influxdb:8086
      INFLUX_BUCKET: xxx
      INFLUX_ORG: org
      INFLUX_TOKEN: xxx
      # マウントポイント
      MOUNT_POINTS: /mnt,/ext

volumes:
  influxdb:
    local: driver
```
