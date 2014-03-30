from tg.controllers.util import LazyUrl
from geopy.geocoders import GoogleV3

earth_radius_km = 6378.137

class JSONLazyUrl(LazyUrl):
    def __json__(self):
        return str(self)


def json_lurl(base_url=None, params=None):
    return JSONLazyUrl(base_url, params)

def coordinate(address):
    if address == "":
        address= "Roma"
    geolocator = GoogleV3()
    address, (latitude, longitude) = geolocator.geocode(address)
    return [longitude, latitude]