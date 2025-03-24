#!/usr/bin/python3

import subprocess
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from vbn_api import request_data

# Configuration
WIDTH, HEIGHT = 320, 480
COLOR_BACK = "skyblue"
COLOR_WESERWEHR = "black"
COLOR_FOEHRENSTR = "red"
NR_DEPARTURES = 12
UPDATE_INTERVAL = 15  # seconds
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
IMAGE_PATH = '/tmp/timetable.png'

STATION_PAIRS = [
    ('1:000009014285', '1:000009013963', COLOR_WESERWEHR),
    ('1:000009014285', '1:000009013884', COLOR_WESERWEHR),
    ('1:000009014285', '1:000009013994', COLOR_WESERWEHR),
    ('1:000009013884', '1:000009014054', COLOR_FOEHRENSTR),
    ('1:000009013884', '1:000009014285', COLOR_FOEHRENSTR),
    ('1:000009013884', '1:000009014184', COLOR_FOEHRENSTR),
]

def get_departures(start, end):
    try:
        return request_data(start=start, end=end)
    except Exception as e:
        print(f"Error fetching departures ({start}->{end}): {e}")
        return []

def prepare_entries(entries, color):
    prepared = []
    current_time = time.time()
    for leg in entries:
        if leg.get("steps") == []:
            route = leg.get("routeShortName")
            headsign = leg.get("headsign")
            start_time = leg.get("startTime")
            if route and headsign and start_time:
                minutes = int((start_time / 1000 - current_time) / 60)
                prepared.append((route, headsign, minutes, color))
    return prepared

# Generate timetable image
def create_timetable_image():
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BACK)
    draw = ImageDraw.Draw(img)
    font_large = ImageFont.truetype(FONT_PATH, 34)
    font_normal = ImageFont.truetype(FONT_PATH, 18)

    current_time_str = datetime.now().strftime("%H:%M")
    draw.text((100, 10), current_time_str, font=font_large, fill="black")

    entries_w, entries_f = [], []

    for start, end, color in STATION_PAIRS[:3]:
        entries_w += prepare_entries(get_departures(start, end), color)

    for start, end, color in STATION_PAIRS[3:]:
        entries_f += prepare_entries(get_departures(start, end), color)

    sorted_entries_w = sorted(entries_w, key=lambda x: x[2])
    sorted_entries_f = sorted(entries_f, key=lambda x: x[2])

    w, f = len(sorted_entries_w), len(sorted_entries_f)
    if w < NR_DEPARTURES // 2 or f < NR_DEPARTURES // 2:
        if w < f:
            f = min(f, NR_DEPARTURES - w)
        elif w > f:
            w = min(w, NR_DEPARTURES - f)
        # else:
            # both are less, all is well
    else:
        f = w = NR_DEPARTURES // 2

    combined_entries = sorted_entries_w[:w] + sorted_entries_f[:f]

    y_offset = 60
    for entry in combined_entries:
        route, dest, minutes, color = entry
        draw.text((5, y_offset), route, font=font_normal, fill=color)
        draw.text((65, y_offset), dest[:12], font=font_normal, fill=color)
        draw.text((250, y_offset), f"{minutes}m", font=font_normal, fill=color)
        y_offset += 35

    img = img.rotate(90, expand=True)
    img.save(IMAGE_PATH)

# Display image to framebuffer
def display_image():
    subprocess.run(['sudo', 'pkill', '-9', 'fbi'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(['sudo', 'fbi', '-noverbose', '-T', '1', '-a', IMAGE_PATH])

# Main daemon loop
if __name__ == "__main__":
    while True:
        create_timetable_image()
        display_image()
        print(f"Updated and displayed at {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(UPDATE_INTERVAL)
