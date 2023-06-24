from typing import Annotated
from fastapi import FastAPI, Query
import requests
import urllib.parse

app = FastAPI()


@app.get("/directions")
async def distance_matrix(key: str, origin: str, container: Annotated[list[str], Query()], destination: str):
    response = await apicall(key, origin, destination, container)

    waypoints = []

    for leg in response["routes"][0]["legs"]:
        waypoint = str(leg["start_location"]["lat"]) + "," + str(leg["start_location"]["lng"])
        waypoints.append(waypoint)

    print(waypoints)

    message = send_telegram(generate_googlemaps_link(origin, destination, waypoints))

    return response


def generate_googlemaps_link(origin, destination, waypoints):
    waypointtxt = ""
    for waypoint in waypoints[1:]:
        waypointtxt += waypoint + "|"
    waypointtxt = waypointtxt[:-1]

    link = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}'.format(origin, destination,
                                                                                                 waypointtxt)
    return link


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


def send_telegram(message):
    token = ""
    chat_id = ""
    url_encoded = urllib.parse.quote(message)
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={url_encoded}"
    print(message)
    # print(requests.get(url).json())

    return message
