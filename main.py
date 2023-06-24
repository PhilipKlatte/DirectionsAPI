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
    durations = await apicall(key, origin, origin, container)

    return durations


async def apicall(key, origin, destination, waypoints):
    baseurl = "https://maps.googleapis.com/maps/api/directions/json"
    originurl = "?origin=" + origin
    destinationurl = "&destination=" + destination
    waypointurls = []
    for waypoint in waypoints:
        waypointurls.append(waypoint + "|")
    optimizeurl = "&optimize=true"
    keyurl = "&key=" + key

    url = baseurl + originurl + destinationurl + "&waypoints="
    for waypointsurl in waypointurls:
        url += waypointsurl
    url = url[:-1]
    url += optimizeurl + keyurl

    response = requests.get(f"{url}")

    return response.json()


def generate_googlemaps_link(route):
    origin = str(route[0]['coordinates'][0]) + ',' + str(route[0]['coordinates'][1])
    waypoints = '|'.join(
        [str(container['coordinates'][0]) + ',' + str(container['coordinates'][1]) for container in route[1:]])

    link = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}'.format(origin, origin,
                                                                                                 waypoints)
    return link