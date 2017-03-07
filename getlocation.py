
import web
import urllib2
import json
import datetime


urls = (

    '/api/weather/current_temperature', 'Temperature',
)



def getlocation(iplocation):
    url = 'http://ipinfo.io/%s/json' % iplocation
    print 'url: ', url
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json.get('loc')
    if location:
        return location.split(',')
    else:
        return None

def getpws(lat, lon):
    f = urllib2.urlopen('http://api.wunderground.com/api/af48603cdc265014/'\
                        'geolookup/q/%s,%s.json' % (lat, lon))
    json_string = f.read()
    parsed_json = json.loads(json_string)
    pws = parsed_json.get('location').get('nearby_weather_stations')\
        .get('pws').get('station')[0].get('id')      
    return pws

def get_temp(pws):
    f = urllib2.urlopen('http://api.wunderground.com/api/'\
                        'af48603cdc265014/conditions/q/pws:%s.json' % pws)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    temp_c = parsed_json.get('current_observation').get('temp_c')
    return temp_c

ipdict = {}
ipdict_time = {}

def return_temp(iplocation):
    location = getlocation(iplocation)
    if location:
        lat = location[0]
        lon = location[1]
        pws = getpws(lat, lon)
        temp_c = get_temp(pws)
        if temp_c:
            ipdict[iplocation] = temp_c
            ipdict_time[iplocation] = datetime.datetime.now()
            print ipdict_time[iplocation]
            return json.dumps({"temperature_c" : temp_c})
    else:
        return "No weather station found in your location."

class Temperature:
    def GET(self):
        iplocation = web.ctx['ip']
        iplocation = '8.8.8.8'
        if iplocation not in ipdict.keys():
            return return_temp(iplocation)
            
        else:
            if (ipdict_time[iplocation] + datetime.timedelta(hours=3)) - datetime.datetime.now() < datetime.timedelta(hours=3):

                return json.dumps({"temperature_c": ipdict.get(iplocation)})
            else:
                return return_temp(iplocation)


    def POST(self):
        return "Temperature"
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

