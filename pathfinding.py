import json
from collections import namedtuple
from urllib2 import urlopen
from Queue import Queue

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

def breadth_first_search(start_point, end_point):
    frontier = Queue()
    frontier.put(start_point)
    came_from = {}
    came_from[start_point] = None

    # Breadth-first traversal of whole grid
    while not frontier.empty():
        current = frontier.get()

        # Stop traversing if we hit the destination
        # BUG: this will never happen if I keep generating
        # the neighbouring points like that
        if current == end_point:
            break

        for nxt in generate_neighbours(current):
            # Only consider points in the sea
            if retrieve_elevation(nxt) <= 0:
                frontier.put(nxt)
                came_from[nxt] = current

    # Trace the path back to get the route
    current = end_point
    path = [current]
    while current != start_point:
        current = came_from[current]
        path.append(current)
    path.reverse()

    return path
