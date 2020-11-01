#!/usr/bin/python3
'''
displays the departures at Bremen Sebaldsbrueck
'''
from tkinter import Tk, Frame, ttk, Label, YES, N, E, S, W, Y
import datetime
from vbn_api import request_data

COLOR_BACK = "sky blue"
COLOR_TEXT = "pale green"
COLOR_TIME = "darkgreen"

# store stations for comparrission
departure_trinidad = ['']*4
departure_sebaldsbrueck = ['']*4


# "1:000009013744", "Bremen Bahnhof Sebaldsbrück (Nord)"
# "1:000009013925", "Bremen Hauptbahnhof"
# "1:000009014238", "Bremen Trinidadstraße"
def get_trinidad_str():
    '''
    retrieves and prepares departuretimes for Trinidadstr
    '''
    departures = request_data()

    return departures

def get_bf_sebaldsbrueck():
    '''
    retrieves and prepares departuretimes for bf_sebaldsbrueck(bus)
    '''
    departures = request_data(start='1:000009013744', end='1:000009013925')

    return departures

def fill():
    '''
    creates and regularly updates interface
    '''
    departure_trinidad_new = get_trinidad_str()
    departure_sebaldsbrueck_new = get_bf_sebaldsbrueck()

    global departure_trinidad, departure_sebaldsbrueck
    
    j = 0
    if departure_trinidad != departure_trinidad_new:
        departure_trinidad = departure_trinidad_new
        for i, start in enumerate(departure_trinidad):
            print(start)
            Label(frame, text=start[0] + " -> " + start[1], font="Helvetica 30 bold", bg=COLOR_BACK).grid(row=i*2)
            Label(frame, text=start[2], fg=COLOR_TIME, font="Courier 20 bold", bg=COLOR_BACK).grid(row=i*2+1, column=0)
            j = i
    if departure_sebaldsbrueck != departure_sebaldsbrueck_new:
        departure_sebaldsbrueck = departure_sebaldsbrueck_new
        for i, start in enumerate(departure_sebaldsbrueck):
            print(start)
            if start[0] == '730':
                Label(frame, text=start[0] + " -> " + start[1], font=("Helvetica 20 bold"), bg=COLOR_BACK).grid(row=j*2)
                Label(frame, text=start[2], font="Courier 16",bg=COLOR_TIME).grid(row=(i+j)*2+1)


    # refresh every 15 Seconds
    frame.after(15000, fill)

# root window
root = Tk()

# switch out for rearranging on other resolution displays
# root.attributes('-fullscreen', True)
root.geometry("480x320")
#hide mouse
root.config(cursor="none", bg=COLOR_BACK)
root.title("departures")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = Frame(root, bg=COLOR_BACK)

frame.grid(row=0, column=0)

#launch
fill()
root.mainloop()
