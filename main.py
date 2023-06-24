from fastapi import FastAPI
import requests
import googlemaps
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/apicall")
async def apicall():
    api = "https://maps.googleapis.com/maps/api/directions/json?destination=Montreal&origin=Toronto&key="
    response = requests.get(f"{api}")
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")
        return "Error occurred"


@app.get("/googledirections")
async def directions():
    now = datetime.now()
    gmaps = googlemaps.Client(key='')

    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)
    print("directions:")
    print(directions_result)
    return directions_result


@app.get("/googledistancematrix")
async def distance_matrix():
    now = datetime.now()
    gmaps = googlemaps.Client(key='')

    fhdw_geocode = gmaps.geocode('Hauptstraße 2, 51465 Bergisch Gladbach')
    dom_geocode = gmaps.geocode('Domkloster 4, 50667 Köln')
    bayarena_geocode = gmaps.geocode('Bismarckstraße 124, 51373 Leverkusen')
    bonn_geocode = gmaps.geocode('Berliner Pl. 2, 53111 Bonn')
    print("geocodes:")
    print(fhdw_geocode)
    print(dom_geocode)
    print(bayarena_geocode)
    print(bonn_geocode)

    directions_result = gmaps.distance_matrix(
                                        origins='Hauptstraße 2, 51465 Bergisch Gladbach',
                                        destinations=[
                                            'Domkloster 4, 50667 Köln',
                                            'Bismarckstraße 124, 51373 Leverkusen',
                                            'Berliner Pl. 2, 53111 Bonn'],
                                        mode="driving",
                                        units="metric",
                                        departure_time=now)

    print(directions_result)
    return directions_result

