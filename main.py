from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import FileResponse
import os

app = FastAPI()

# API Key OpenWeatherMap
API_KEY = 'd351751ed0a133daa78378b4c7e80b2b'


class City(BaseModel):
    name: str


@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join(os.getcwd(), "index.html"))


@app.post("/weather")
def get_weather(city: City):
    city_name = city.name
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"

    current_response = requests.get(current_weather_url)
    if current_response.status_code != 200:
        raise HTTPException(status_code=current_response.status_code, detail="Error fetching weather data")

    current_data = current_response.json()
    current_weather = {
        "temperature": current_data["main"]["temp"],
        "description": current_data["weather"][0]["description"],
        "city": city_name,
        "country": current_data["sys"]["country"]
    }

    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        raise HTTPException(status_code=forecast_response.status_code, detail="Error fetching forecast data")

    forecast_data = forecast_response.json()
    forecast = [{
        "date": item["dt_txt"],
        "temperature": item["main"]["temp"],
        "description": item["weather"][0]["description"]
    } for item in forecast_data["list"]]

    return {"current_weather": current_weather, "forecast": forecast}

# https://openweathermap.org/forecast5#list
# https://openweathermap.org/current#min
