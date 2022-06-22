import asyncio
import os

import psutil
from aiohttp import ClientSession

interval = int(os.getenv("INTERVAL"))
influx_addr = os.getenv("INFLUX_ADDR")
influx_bucket = os.getenv("INFLUX_BUCKET")
influx_org = os.getenv("INFLUX_ORG")
influx_token = os.getenv("INFLUX_TOKEN")
mount_points = os.getenv("MOUNT_POINTS").split(",")

async def main():
    while True:
        await handle()
        await asyncio.sleep(interval)

async def handle():
    await write_cpu_freq()
    await write_disk_usage()

async def write_cpu_freq():
    await asyncio.gather(
        *[write(f"cpufreq,cpu={i}", cpu._asdict()) for i, cpu in enumerate(psutil.cpu_freq(percpu=True))]
    )

async def write_disk_usage():
    await asyncio.gather(
        *[write(f"diskusage,mount={x}", psutil.disk_usage(x)._asdict()) for x in [f"{z}/{y}" for z in mount_points for y in os.listdir(z)] if os.path.isdir(x)]
    )

async def write(measurement, data):
    async with ClientSession(raise_for_status=True) as session:
        line = f"{measurement} " + ",".join([f"{k}={v}" for k, v in data.items()])
        headers = {
            "Authorization": f"Token {influx_token}"
        }

        async with session.post(f"{influx_addr}/api/v2/write?bucket={influx_bucket}&org={influx_org}&precision=s", data=line, headers=headers):
            print(f"Write: {line}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
