#!/usr/bin/python3
'''
displays the departures at Bremen Sebaldsbrueck
'''
from tkinter import Tk, Frame, ttk, Label, YES, N, E, S, W, Y
import datetime
from vbn_api import request_data
import time
from datetime import datetime

COLOR_BACK = "sky blue"
COLOR_TEXT_T = "pale green"
COLOR_TIME_T = "darkgreen"
COLOR_TEXT_B = "darkolovegreen"
COLOR_TIME_B = "red"

# store stations for comparrission
departure_sebaldsbrueck = []
frame = None

# "1:000009013744", "Bremen Bahnhof Sebaldsbrück (Nord)"
# "1:000009013925", "Bremen Hauptbahnhof"
def get_bf_sebaldsbrueck():
    '''
    retrieves and prepares departuretimes for bf_sebaldsbrueck(bus)
    '''
    return request_data(start='1:000009013744', end='1:000009013925')
    
def fill():
    '''
    creates and regularly updates interface
    '''
    global departure_sebaldsbrueck, frame

    try:
        departure_sebaldsbrueck = get_bf_sebaldsbrueck()
    except:
        departure_sebaldsbrueck = []

    # store departures to check for and avoid doubles
    NR_DEPARTURES = 12
    departures = []
    departures_old = [""]*NR_DEPARTURES
    i = 0
    
    frame=Frame(root, bg=COLOR_BACK, width=320, height=480)
    print(datetime.now().strftime("%H:%M"))
    root.title("vbn GUI")
    Label(text=datetime.now().strftime("%H:%M"), font="Helvetica 34 bold", bg=COLOR_BACK).place(x=100, y=10)
    i += 1


    if len(departure_sebaldsbrueck) == 0:
        Label(text="                                        ", font="Helvetica 34 bold", bg=COLOR_BACK).place(x=00, y=50)
        Label(text="keine Daten", font="Helvetica 30 bold", bg=COLOR_BACK).place(x=30, y=50)
        for i in range(10):
            Label(text="                                        ", font="Helvetica 21 bold", bg=COLOR_BACK).place(x=00, y=80 + (i)*40)


    else:
        entries = []

        if len(departure_sebaldsbrueck) != 0:
            for leg in departure_sebaldsbrueck:
                print(leg)
                # avoid transfer
                if leg.get("steps") == []:
                    if "routeShortName" in leg and "headsign" in leg and "startTime" in leg:
                        entries.append((leg.get("routeShortName"), leg.get("headsign"), int((leg.get("startTime")/1000 - time.time())/60)))

        sorted_entries = []
        if(len(entries) != 0):
            sorted_entries = sorted(entries, key=lambda x: x[2])
            for i, entry in enumerate(sorted_entries):
                if (i < NR_DEPARTURES):
                    zielbahnhof = entry[1]
                    if len(zielbahnhof) > 12:
                        zielbahnhof = zielbahnhof[:12]
                    if len(zielbahnhof) <12:
                        for _ in range(12-len(zielbahnhof)):
                            zielbahnhof += " "
                    departure = str(entry[2])
                    if len(departure) <4:
                        if len(departure) <3:
                            if len(departure) <2:
                                departure = " "+(departure)
                            departure = " "+(departure)
                        departure = " "+(departure)
                    text_ = ""
                    text_ += entry[0] + "->" + zielbahnhof + ":" + departure
                    if departures_old[i] != text_:
                        departures_old[i] = text_
                        Label(text="                                        ", font="Helvetica 21 bold", bg=COLOR_BACK).place(x=00, y=60 + (i)*40)
                        Label(text=text_, font="Helvetica 21 bold", bg=COLOR_BACK).place(x=00, y=60 + (i)*40)
            for i in range(len(sorted_entries), NR_DEPARTURES, 1):
                Label(text="                                        ", font="Helvetica 21 bold", bg=COLOR_BACK).place(x=00, y=60 + (i)*40)




    # refresh every 5 Seconds
    frame.after(5000, fill)

# root window
root = Tk()

# switch out for rearranging on other resolution displays
root.attributes('-fullscreen', True)
root.geometry("320x480")
#hide mouse
root.config(cursor="none", bg=COLOR_BACK)
root.title("departures")
frame=Frame(root, bg=COLOR_BACK, width=320, height=480)

#launch
fill()
root.mainloop()
