import json
from collections import namedtuple
from urllib2 import urlopen
from Queue import PriorityQueue
from math import sin, cos, asin, atan2, sqrt, radians, pi, degrees

GeoPoint = namedtuple('GeoPoint', ['lat', 'lng'])

start = GeoPoint(-33, 151) # approx Sydney
end   = GeoPoint(-44, 176) # approx Chatham Islands

def generate_neighbours(point):
    lat = point.lat
    lng = point.lng
    return [GeoPoint(lat + 1, lng),
            GeoPoint(lat - 1, lng),
            GeoPoint(lat, lng + 1),
            GeoPoint(lat, lng - 1)]

def retrieve_elevation(point):
    base_url = 'http://maps.googleapis.com/maps/api/elevation/'
    query_str = 'json?locations=' + str(point.lat) + ',' + str(point.lng)
    query_url = base_url + query_str
    response = urlopen(query_url).read()
    return json.loads(response)['results'][0]['elevation']

def retrieve_elevation_test(point):
    return 0

def point_from_origin(origin, bearing, dist='km'):
    """Return the point the specified distance from the origin point,
    that lies on the given radial.

    :type origin: GeoPoint
    :type radial: integer
    :type dist: integer
    """
    p1 = radians(origin.lat)
    l1 = radians(origin.lng)
    ad = dist / 6371
    b = radians(bearing)

    p2 = asin(sin(p1) * cos(ad) + \
              cos(p1) * sin(ad) * cos(b))
    l2 = l1 + atan2(sin(b) * sin(ad) * cos(p1),
                    cos(ad) - sin(p1) * sin(p2))
    l2 = (l2 + 3 * pi) % (2 * pi) - pi

    return GeoPoint(degrees(p2), degrees(l2))

def haversine(a, b, unit='m', roundto=3):
    """Calculate the great-circle distance between a and b in metres.

    :type a: GeoPoint
    :type b: Geopoint
    :param unit: Metric unit to return distance in
    :type unit: string
    :param roundto: Number of decimal places to round distance
    :type roundto: integer
    """
    R      = 6371000 # The mean radius of the earth in metres
    p1     = radians(a.lat)
    p2     = radians(b.lat)
    dp = radians(b.lat - a.lat)
    dl = radians(b.lng - a.lng)

    a = sin(dp / 2) * sin(dp / 2) + cos(p1) * cos(p2) * sin(dl / 2) * sin(dl / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c

    if unit == 'm':
        return round(d, roundto)

    elif unit == 'km':
        return round(d / 1000, roundto)

    else:
        raise ValueError('Invalid unit specified')


def find_sea_route(start, end):

    # A* search
    frontier = PriorityQueue()
    frontier.put(start, 0)
    parent = {}
    parent[start] = None

    while not frontier.empty():
        current = frontier.get()
        if haversine(current, end, 'km') < 10:
            break
        for point in generate_neighbours(current):
            if point not in parent and retrieve_elevation_test(point) <= 0:
                frontier.put(point, haversine(point, end, 'km'))
                parent[point] = current

    # Walk backwards to build the path
    path = [current]
    while current != start:
        current = parent[current]
        path.append(current)

    return path
