import sys
import pycurl
import time
import re
import json

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

# curl -X GET   'http://gtfsr.vbn.de/api/routers/connect/plan?arriveBy=false&date=02-14-2025&fromPlace=53.059429,8.899465&toPlace=53.051735,8.819698&time=13:00:00&mode=WALK,TRANSIT&maxWalkDistance=300'   -H 'Authorization: --'   -H 'Host: gtfsr.vbn.de'

def create_header():
    # can be requested via email from vbn
    header = ['Authorization: --']
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
        #haltestellenid = Bahnhof Sebaldsbrück
        start = '1:000009013744'
    if end is None:
        #Haltestellenid = Bremen HBF
        end = '1:000009013925'

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
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 5)

    try:
        c.perform()
        c.close()
    except Exception as e:
        print('exeption: ')
        print(e)
        print("returned")
        return []
    data = json.loads(buffer.getvalue())
    legs = []
    if(len(data) != 0):
        for trip in list(data.get('plan').get('itineraries')):
            leg = trip.get("legs")[0]
            legs.append(leg)
        return legs
    return []