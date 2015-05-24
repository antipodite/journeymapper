import json
import math
from collections import namedtuple
from urllib2 import urlopen
from Queue import PriorityQueue

GeoPoint = namedtuple('GeoPoint', ['lat', 'lng'])

start = GeoPoint(lat=-36, lng=174)
end   = GeoPoint(lat=-41, lng=174)

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

def retrieve_elevation_test():
    return 0

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
    p1     = math.radians(a.lat)
    p2     = math.radians(b.lat)
    dp = math.radians(b.lat - a.lat)
    dl = math.radians(b.lng - a.lng)

    a = math.sin(dp / 2) * math.sin(dp / 2) + \
        math.cos(p1) * math.cos(p2) * \
        math.sin(dl / 2) * math.sin(dl / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    if unit == 'm':
        return round(d, roundto)

    elif unit == 'km':
        return round(d / 1000, roundto)

    else:
        raise ValueError('Invalid unit specified')


# A couple of ideas for this:
# - use A* to minimise the number of unecessary queries
# - If points are near, use smaller grid, if far, larger
# - Try different grid spacings to see what makes the nicest path
# - Find out how to draw a curved Gmaps polyline
# - Use a downloaded data set to allow finer resolution pathfinding, since
#   I'm going to precompute the paths anyway
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
            if point not in came_from and retrieve_elevation_test(n) <= 0:
                frontier.put(point, haversine(point, end, 'km'))
                parent[point] = current

    # Walk backwards to build the path
    path = [current]
    while current != start_point:
        current = came_from[current]
        path.append(current)

    return path
