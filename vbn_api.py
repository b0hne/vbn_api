import sys
import pycurl
import time
import re
from eventlet import Timeout

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

def create_header():
    # can be requested via email
    header = ['Authorization: ...']
    header.append('Host: gtfsr.vbn.de')
    return header

def request_data(start_time=None, date=None, start=None, end=None):
    header = create_header()

    t = time.localtime()
    if date is None:
        date = time.strftime("%Y-%m-%d", t)
    if start_time is None:
        start_time = time.strftime("%H:%M:%S", t)
    if start is None:
        #haltestellenid = Trinidadstr
        start = '1:000009014238'
    if end is None:
        #Haltestellenid = Bahnhof Sebaldsbrück
        end = '1:000009013744'

    buffer = BytesIO()
    c = pycurl.Curl()
    address = 'http://gtfsr.vbn.de/api/'
    address += ('routers/connect/plan?arriveBy=false'
                'time={0}'
                '&date={1}'
                '&fromPlace={2}'
                '&toPlace={3}').format(start_time, date, start, end)
    c.setopt(c.URL, address)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.WRITEDATA, buffer)
    passed = False
    with Timeout(4, False):
        try:
            c.perform()
            c.close()
            passed = True
        except Exception as e:
            print('exeption: ')
            print(e)
    if passed:
        body = buffer.getvalue().decode('UTF8')
        return prepare_data(body)
    else:
        return []

# return list of ['Strassenbahnnummer', 'Endhaltestelle',
#                 'Zeit bis Abfahrt', 'Verspätung in Sekunden]
def prepare_data(data):
    stops = re.findall("\"legs\"\:\[(.*?)\]\,", data)
    starts = []
    i = 0
    for stop in stops:
        mode = re.findall("mode\"\:\"(.*?)\"\,", stop)
        route = re.findall("route\"\:\"(.*?)\"\,", stop)
        headsign = re.findall("headsign\"\:\"(.*?)\"\,", stop)
        s_time = re.findall("startTime\"\:(.*?)\,", stop)
        time_left = (time.asctime(time.gmtime(int(s_time[0][0:10])
                     - time.time()))[10:16])
        delay = re.findall("departureDelay\"\:(.*?)\,", stop)

        if len(mode) > 1 and mode[1] == 'RAIL':
            starts.append([route[1]])
            starts[i].extend(headsign)
            starts[i].extend([time_left])
            starts[i].extend([delay[1]])
            i += 1
        elif mode[0] != 'WALK':
            starts.append(route)
            starts[i].extend(headsign)
            starts[i].extend([time_left])
            starts[i].extend(delay)
            i += 1

    return(starts)
