import json
import time

import psutil
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, sh1107
from PIL import ImageFont

first = sh1106(i2c(port=4, address=0x3C))
second = sh1107(i2c(port=5, address=0x3C), width=128, height=128)


robot = ImageFont.truetype(
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf", 16
)
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf", 14
)
THERMAL_PATH = "/sys/class/thermal/thermal_zone0/temp"


def get_stats():
    try:
        with open(THERMAL_PATH, "r") as f:
            temp = f.read()
            temp = str(round((int(temp) / 1000), 1)) + "°C"
    except (FileNotFoundError, PermissionError):
        temp = "N/A"

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    return temp, cpu, mem


old_stats = psutil.net_io_counters()


def get_inet_stats():
    global old_stats
    fresh_stats = psutil.net_io_counters()
    bytes_sent_per_sec = fresh_stats.bytes_sent - old_stats.bytes_sent
    bytes_recv_per_sec = fresh_stats.bytes_recv - old_stats.bytes_recv

    mb_sent = bytes_sent_per_sec * 8
    mb_recv = bytes_recv_per_sec * 8

    old_stats = fresh_stats

    return mb_recv, mb_sent


def get_battery_info():
    with open("data.json", "r") as f:
        data = json.load(f)
    consumption = data.get("watt")
    percent = data.get("ups_percent")
    power_state = data.get("power_state")

    return percent, consumption, power_state


def write_second_oled(recv: int, sent: int) -> None:
    if recv >= 1_000_000:
        recv_string = f"{recv / 1_000_000:.1f}Mbps"
    else:
        recv_string = f"{recv / 1_000:.1f}Kbps"

    if sent >= 1_000_000:
        sent_string = f"{sent / 1_000_000:.1f}Mbps"
    else:
        sent_string = f"{sent / 1_000:.1f}Kbps"

    with canvas(second) as draw:
        draw.rectangle(second.bounding_box, outline="white", fill="black")
        draw.text((5, 2), f"D\u2193|{recv_string}", fill="white", font=robot)
        draw.line((0, 24, 128, 24), fill=255, width=1)
        draw.text((5, 26), f"U\u2191|{sent_string}", fill="white", font=robot)
        draw.line((0, 47, 128, 47), fill=255, width=1)


def write_first_oled(battery: float, power: float, state: str) -> None:
    with canvas(first) as draw:
        draw.rectangle(first.bounding_box, outline="white", fill="black")
        draw.text((5, 5), f"Battery {battery}%", fill="white", font=font)
        draw.text((5, 23), f"Power {power} W", fill="white", font=font)
        draw.text((5, 41), f"State {state}", fill="white", font=font)


is_night = False

while True:
    current_hour = time.localtime().tm_hour
    now_should_be_night = current_hour >= 22 or current_hour < 7
    if now_should_be_night != is_night:
        is_night = now_should_be_night
        new_contrast = 10 if is_night else 220

        first.contrast(new_contrast)
        second.contrast(new_contrast)

    percent, consumption, power_state = get_battery_info()
    recv, sent = get_inet_stats()

    write_first_oled(battery=percent, power=consumption, state=power_state)
    write_second_oled(recv=recv, sent=sent)
    time.sleep(1)
