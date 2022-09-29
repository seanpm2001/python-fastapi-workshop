import json
import pathlib

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Restaurant API")


@app.get("/")
def hello_world():
    return {"Hello": "Jerry"}


@app.get(
    "/showcase-features/{user_id}",
    summary="MY custom summary",
    description="My custom description",
)
def showcase_features(
    user_id: int = Path(description="my custom description"),
    debug: bool = Query(default=False, description="some description"),
):
    if debug:
        print("Now we are debugging")
    return {"foo": "bar", "user_id": user_id}


"""
[
  {
    "name": "Example restaurant",
    "description": "Example description",
    "id": "unique-id-for-the-restaurant",
    "location": {
      "city": "Example city",
      "coordinates": {
        "lat": 60.169938852212965,
        "lon": 24.941325187683105
      }
    }
  }
]
"""


class Location(BaseModel):
    city: str


class Restaurant(BaseModel):
    name: str = Field(description="This is the name of the restaurant")
    description: str
    id: str
    location: Location


@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants():
    data_file_path = pathlib.Path(__file__).parent / "restaurants.json"

    with open(data_file_path) as f:
        raw_data = json.load(f)

    restaurants = []
    for raw_restaurant in raw_data["restaurants"]:
        restaurant = Restaurant(
            name=raw_restaurant["name"],
            description=raw_restaurant["description"],
            id=raw_restaurant["id"],
            location=Location(city=raw_restaurant["city"]),
        )
        restaurants.append(restaurant)
    return restaurants
