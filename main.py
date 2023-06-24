from typing import Annotated

from fastapi import FastAPI, Query
import requests
import googlemaps
from datetime import datetime

app = FastAPI()


@app.get("/directions")
async def distance_matrix(key: str, origin: str, destination: Annotated[list[str], Query()]):
    now = datetime.now()
    gmaps = googlemaps.Client(key=key)

    directions_result = gmaps.distance_matrix(
                                        origins=origin,
                                        destinations=destination,
                                        mode="driving",
                                        units="metric",
                                        departure_time=now)

    print(directions_result)
    return directions_result

