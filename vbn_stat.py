#!/usr/bin/python3
'''
displays the departures at Bremen Sebaldsbrueck
'''
from tkinter import Tk, Frame, ttk, Label, YES, N, E, S, W, Y
import datetime
from vbn_api import request_data
from time import sleep
from datetime import datetime

COLOR_BACK = "sky blue"
COLOR_TEXT_T = "pale green"
COLOR_TIME_T = "darkgreen"
COLOR_TEXT_B = "darkolovegreen"
COLOR_TIME_B = "red"

# store stations for comparrission
departure_trinidad = []
departure_sebaldsbrueck = []
frame = None


# "1:000009013744", "Bremen Bahnhof Sebaldsbrück (Nord)"
# "1:000009013925", "Bremen Hauptbahnhof"
# "1:000009014238", "Bremen Trinidadstraße"
def get_trinidad_str():
    '''
    retrieves and prepares departuretimes for Trinidadstr
    '''
    departures = request_data()
    # if departures == [' ']*4:
    #     return []
    return departures

def get_bf_sebaldsbrueck():
    '''
    retrieves and prepares departuretimes for bf_sebaldsbrueck(bus)
    '''
    departures = request_data(start='1:000009013744', end='1:000009013925')
    # if departures == [' ']*4:
    #     return []
    return departures

def fill():
    '''
    creates and regularly updates interface
    '''
    global departure_trinidad, departure_sebaldsbrueck, frame

    # store departures to check for and avoid doubles
    departures = []
    i = 0
    for widget in frame.winfo_children():
        widget.destroy()

    print(datetime.now().strftime("%H:%M"))
    root.title("Python GUI")
    Label(frame, text=datetime.now().strftime("%H:%M"), font="Helvetica 34 bold", bg=COLOR_BACK).grid(row=i)
    i += 1
    Label(frame, text='', font="Helvetica 24 bold", bg=COLOR_BACK).grid(row=i)
    i += 1

    departure_trinidad = get_trinidad_str()
    departure_sebaldsbrueck = get_bf_sebaldsbrueck()

    if len(departure_sebaldsbrueck) == 0 or len(departure_trinidad) == 0:
        label_text = "keine Daten"
        Label(frame, text=label_text, font="Helvetica 24 bold", bg=COLOR_BACK).grid(row=i)
        return
    else:
        for start in departure_trinidad:
            departures.append(start[0])
            label_text = start[0] + " -> " + start[1]
            label_length = len(label_text)
            if label_length > 18:
                label_text = label_text[:18]
            print("i: ", i)
            Label(frame, text=label_text, font="Helvetica 24 bold", bg=COLOR_BACK).grid(row=i)
            i += 1
            Label(frame, text=start[2], fg=COLOR_TIME_T, font="Courier 20 bold", bg=COLOR_BACK).grid(row=i)
            i += 1

        for start in departure_sebaldsbrueck:
            if not start[0] in departures:
                label_text = start[0] + " -> " + start[1]
                label_length = len(label_text)
                if label_length > 18:
                    label_text = label_text[:18]
                Label(frame, text=label_text, font=("Helvetica 24 bold"), bg=COLOR_BACK).grid(row=i)
                i += 1
                Label(frame, text=start[2], font="Courier 20 bold",bg=COLOR_BACK, fg=COLOR_TIME_B).grid(row=i)
                i += 1


    # refresh every 15 Seconds
    frame.after(15000, fill)

# root window
root = Tk()

# switch out for rearranging on other resolution displays
root.attributes('-fullscreen', True)
root.geometry("320x480")
#hide mouse
root.config(cursor="none", bg=COLOR_BACK)
root.title("departures")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = Frame(root, bg=COLOR_BACK)
frame.grid(row=0, column=0, sticky="n")

#launch
fill()
root.mainloop()


