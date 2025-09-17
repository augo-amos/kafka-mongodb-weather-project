import os
import json
from datetime import datetime, timezone
from kafka import KafkaConsumer
from pymongo import MongoClient

# Correct MongoDB URI - note the "/weather_db" after .net
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://weather-user:hpisvVCLJYS37pZw@cluster0.769sgus.mongodb.net/weather_db?retryWrites=true&w=majority&appName=Cluster0"
)

# Connect to Atlas
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["weather_db"]
collection = db["weather_data"]

# Kafka consumer
consumer = KafkaConsumer(
    "weather_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("listening to weather_data")

for message in consumer:
    data = message.value

    doc = {
        "city": data["city"],
        "temp": data["temp"],
        "humidity": data["humidity"],
        "condition": data["condition"],
        "timestamp": data["timestamp"],
        "timestamp_dt": datetime.fromtimestamp(int(data["timestamp"]), tz=timezone.utc),
        "ingested_at": datetime.now(timezone.utc)
    }

    collection.insert_one(doc)
    print(f"Inserted into Atlas: {doc}")
