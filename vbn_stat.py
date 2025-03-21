#!/usr/bin/python3
'''
Displays the departures at Bremen Weserwehr and Föhrenstraße with subdivided labels for route, destination, and minutes
'''
import time
from tkinter import Tk, Label
from datetime import datetime
from vbn_api import request_data

# GUI Configuration
COLOR_BACK = "sky blue"  # Background color
COLOR_WESERWEHR = "black"  # Default text color
COLOR_FÖHRENSTR = "red"      # Alert text color
NR_DEPARTURES = 12       # Number of departure entries displayed
UPDATE_INTERVAL = 5000   # Update interval in milliseconds (5 seconds)

# Station pairs and their display colors
STATION_PAIRS = [
    ('1:000009014285', '1:000009013963', COLOR_WESERWEHR),  # Weserwehr - Hohwisch
    ('1:000009014285', '1:000009013884', COLOR_WESERWEHR),  # Weserwehr - Föhrenstraße
    ('1:000009014285', '1:000009013994', COLOR_WESERWEHR),  # Weserwehr - Karl-Carstens-Brücke
    ('1:000009013884', '1:000009014054', COLOR_FÖHRENSTR),    # Föhrenstraße - Malerstraße
    ('1:000009013884', '1:000009014285', COLOR_FÖHRENSTR),    # Föhrenstraße - Weserwehr
    ('1:000009013884', '1:000009014184', COLOR_FÖHRENSTR),    # Föhrenstraße - Sebaldsbrück
]

# Setup GUI window
root = Tk()
root.geometry("320x480")
root.config(cursor="none", bg=COLOR_BACK)
root.title("vbn GUI")

# Initialize labels subdivided into route, destination, and minutes
route_labels = [Label(root, text="", font="Helvetica 18 bold", bg=COLOR_BACK, width=5, anchor='w') for _ in range(NR_DEPARTURES)]
dest_labels = [Label(root, text="", font="Helvetica 18 bold", bg=COLOR_BACK, width=14, anchor='w') for _ in range(NR_DEPARTURES)]
time_labels = [Label(root, text="", font="Helvetica 18 bold", bg=COLOR_BACK, width=5, anchor='e') for _ in range(NR_DEPARTURES)]

for i in range(NR_DEPARTURES):
    route_labels[i].place(x=5, y=60 + i * 35)
    dest_labels[i].place(x=65, y=60 + i * 35)
    time_labels[i].place(x=250, y=60 + i * 35)

# Label to display the current time
time_label = Label(root, text="", font="Helvetica 34 bold", bg=COLOR_BACK)
time_label.place(x=100, y=10)

# Retrieve departure data for given stations
def get_departures(start, end):
    try:
        return request_data(start=start, end=end)
    except Exception as e:
        print(f"Error fetching departures ({start}->{end}): {e}")
        return []

# Prepare entries by filtering and formatting data
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

# Update the GUI with latest departure information
def update_display():
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
    else:
        f = w = NR_DEPARTURES // 2

    combined_entries = sorted_entries_w[:w] + sorted_entries_f[:f]

    for i, entry in enumerate(combined_entries):
        route_labels[i].config(text=entry[0], fg=entry[3])
        dest_labels[i].config(text=entry[1][:12], fg=entry[3])
        time_labels[i].config(text=f"{entry[2]}", fg=entry[3])

    for i in range(len(combined_entries), NR_DEPARTURES):
        route_labels[i].config(text="")
        dest_labels[i].config(text="")
        time_labels[i].config(text="")

    time_label.config(text=datetime.now().strftime("%H:%M"))

    root.after(UPDATE_INTERVAL, update_display)
    print("update")

# Start updating loop
update_display()
root.mainloop()