from tg.controllers.util import LazyUrl
import urllib, urllib2

class JSONLazyUrl(LazyUrl):
    def __json__(self):
        return str(self)


def json_lurl(base_url=None, params=None):
    return JSONLazyUrl(base_url, params)

def coordinate(address):
    address_list=[address]
    if len(address_list) > 25:
        print "25 records maximum per request"
        raise

    url = "http://maps.google.com/maps?f=d&hl=en&%s&ie=UTF8&0&om=0&output=html"\
        % ("saddr=" + "%20to:".join([urllib.quote(record)for record in address_list]))

    opener = urllib2.build_opener()
    page = opener.open(url).read()
    list_mark = page.split(",latlng:{")[1:]

    list_coordinate = [ mark[0:mark.find('},image:')].replace("lat:","").replace("lng:","") for mark in list_mark]

    array = str(list_coordinate).replace("'", "").replace("]","").replace("[","").split(",")
    return [float(array[1]),float(array[0])]