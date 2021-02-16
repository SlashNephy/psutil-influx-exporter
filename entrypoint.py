import asyncio
import os

import psutil
from aiohttp import ClientSession

interval = int(os.getenv("INTERVAL"))
influx_addr = os.getenv("INFLUX_ADDR")
influx_db = os.getenv("INFLUX_DB")
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

        async with session.post(f"{influx_addr}/write?db={influx_db}&precision=s", data=line):
            print(f"Write: {line}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
