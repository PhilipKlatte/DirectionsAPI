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
    points = [origin]

    for elem in container:
        points.append(elem)

    durations = await apicall(key, origin, container)
    print(durations)

    container_permutations = list(itertools.permutations(container))

    possible_ways = []

    for container_permutation in container_permutations:
        possible_way = [origin]

        for elem in container_permutation:
            possible_way.append(elem)

        possible_ways.append(possible_way)

    return durations


def get_durations(key, origin, destinations):
    now = datetime.now()
    gmaps = googlemaps.Client(key=key)

    return gmaps.distance_matrix(
        origins=origin,
        destinations=destinations,
        mode="driving",
        units="metric",
        departure_time=now,
        optimize=True)


async def apicall(key, origin, destinations):
    baseurl = "https://maps.googleapis.com/maps/api/directions/json"
    originurl = "?origin=" + origin
    destinationurl = "&destination=50.958544,7.192955"
    waypointsurl = "&waypoints=50.983998,7.119667|50.993660,7.146680|50.994460,7.117352"
    optimizeurl = "&optimize=true"
    keyurl = "&key=" + key

    url = baseurl + originurl + destinationurl + waypointsurl + optimizeurl + keyurl

    response = requests.get(f"{url}")
    return response.json()


def generate_googlemaps_link(route):
    origin = str(route[0]['coordinates'][0]) + ',' + str(route[0]['coordinates'][1])
    waypoints = '|'.join(
        [str(container['coordinates'][0]) + ',' + str(container['coordinates'][1]) for container in route[1:]])

    link = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}'.format(origin, origin,
                                                                                                 waypoints)
    return link