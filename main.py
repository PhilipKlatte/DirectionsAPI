from typing import Annotated
from fastapi import FastAPI, Query
import requests
import googlemaps
from datetime import datetime
import itertools
import requests
import telegram
import requests
import urllib.parse

app = FastAPI()


@app.get("/directions")
async def distance_matrix(key: str, origin: str, container: Annotated[list[str], Query()]):
    points = container
    points.append(origin)

    generate_route(points)

    now = datetime.now()
    gmaps = googlemaps.Client(key=key)

    directions_result = gmaps.distance_matrix(
        origins=origin,
        destinations=container,
        mode="driving",
        units="metric",
        departure_time=now)

    print(directions_result)
    return directions_result


def generate_route(points):
    point_combinations = list(itertools.permutations(points[1:]))
    optimal_route = []
    shortest_distance = float('inf')

    for combination in point_combinations:
        total_distance = 0
        ordered_combination = [points[0]] + list(points)




        if total_distance < shortest_distance:
            shortest_distance = total_distance
            optimal_route = ordered_combination

    return optimal_route


def generate_googlemaps_link(route):
    origin = str(route[0]['coordinates'][0]) + ',' + str(route[0]['coordinates'][1])
    waypoints = '|'.join(
        [str(container['coordinates'][0]) + ',' + str(container['coordinates'][1]) for container in route[1:]])

    link = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}'.format(origin, origin,
                                                                                                 waypoints)
    return link


# Beispielaufruf
start_point = {'id': 0, 'coordinates': (50.958544, 7.192955)}  # Hier kannst du die Koordinaten des Startpunkts eingeben
containers = [
    start_point,
    {'id': 1, 'coordinates': (50.983998, 7.119667)},
    {'id': 2, 'coordinates': (50.993660, 7.146680)},
    {'id': 3, 'coordinates': (50.994460, 7.117352)}
]

route = generate_route(containers)
googlemaps_link = generate_googlemaps_link(route)

print("Optimale Reihenfolge der Container:", [container['id'] for container in route])
print("Google Maps Link zur Route:", googlemaps_link)

TOKEN = ""
chat_id = ""
message = googlemaps_link
url_encoded = urllib.parse.quote(message)
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={url_encoded}"
# print(requests.get(url).json()) # this sends the message
