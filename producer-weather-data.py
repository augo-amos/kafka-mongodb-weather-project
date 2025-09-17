import requests 
import time
from kafka import KafkaProducer 
import json 
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env


API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ['Nairobi', 'Nakuru', 'Eldoret', 'Dodoma']

producer = KafkaProducer(
    bootstrap_servers= "localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "weather_data"

while True: 
    for city in CITIES:
        try:
            url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            payload = {
                "city": city,
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["main"],
                "timestamp": data["dt"]
            }
            producer.send(topic, value = payload) 
            print(f"sent: {payload}")
        except Exception as e:
            print("Error!: ", e)


        time.sleep(10)


