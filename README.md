
```markdown
# Kafka Weather Data Pipeline with MongoDB Atlas

This project demonstrates how to build a simple **data pipeline** that fetches real-time weather data from the [OpenWeatherMap API](https://openweathermap.org/api), publishes it to an **Apache Kafka topic**, consumes it, and stores it in **MongoDB Atlas (cloud database)** for analysis.

---

## Features
- Fetch live weather data for multiple cities using OpenWeatherMap API.
- Publish data to Kafka in JSON format.
- Consume data from Kafka and insert into MongoDB Atlas.
- Store timestamps as timezone-aware `datetime` objects for easier querying.
- Example queries for exploring and analyzing weather trends.

---

## Project Structure
```

kafka-weather-project/
│
├── producer-weather-data.py       # Fetches weather data and publishes to Kafka
├── consumer-weather-analysis.py   # Consumes data and prints simple analysis
├── mongo-consumer-weather-data.py # Consumes data and inserts into MongoDB Atlas
├── test-mongo-connection.py       # Script to test MongoDB Atlas connection
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation (this file)

````

---

## Prerequisites
Before you begin, ensure you have:

1. **Python 3.10+**
2. **Kafka & Zookeeper** running locally on default ports:
   - Kafka broker → `localhost:9092`
   - Zookeeper → `localhost:2181`
3. **MongoDB Atlas account** (free cluster is enough)
4. **OpenWeatherMap API Key** → [Sign up here](https://home.openweathermap.org/users/sign_up)

---

## Installation

Clone the repository:
```bash
git clone https://github.com/your-username/kafka-weather-project.git
cd kafka-weather-project
````

Create a virtual environment:

```bash
python3 -m venv kaf-env
source kaf-env/bin/activate   # On Windows: kaf-env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
requests
kafka-python
pymongo
```

---

## Usage

### 1. Start Kafka

Open a terminal and start Zookeeper:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Then start Kafka broker:

```bash
bin/kafka-server-start.sh config/server.properties
```

### 2. Run Producer

Fetches weather data and sends it to Kafka:

```bash
python producer-weather-data.py
```

Sample output:

```
sent: {'city': 'Nairobi', 'temp': 22.1, 'humidity': 68, 'condition': 'Clouds', 'timestamp': 1694567890}
```

### 3. Run Consumer with MongoDB Atlas

Consumes weather data and inserts into MongoDB:

```bash
python mongo-consumer-weather-data.py
```

Sample output:

```
Inserted into Atlas: {'city': 'Nairobi', 'temp': 22.1, 'humidity': 68, 'condition': 'Clouds', 'timestamp': 1694567890, 'timestamp_dt': datetime.datetime(2023, 9, 13, 12, 58, tzinfo=datetime.timezone.utc), 'ingested_at': datetime.datetime(2023, 9, 13, 13, 0, tzinfo=datetime.timezone.utc)}
```

---

## MongoDB Atlas Setup

1. Sign in to [MongoDB Atlas](https://cloud.mongodb.com).
2. Create a **free cluster**.
3. Under **Database Access**:

   * Create a user, e.g., `weather_user` with **Read and write** privileges.
4. Under **Network Access**:

   * Allow access from `0.0.0.0/0` (or your IP).
5. Copy the connection string from Atlas → **Connect → Drivers → Python**.

   * Example:

     ```
     mongodb+srv://weather_user:YourPassword@cluster0.abcde.mongodb.net/weather_db?retryWrites=true&w=majority
     ```
6. Replace in `mongo-consumer-weather-data.py`:

   ```python
   MONGO_URI = "mongodb+srv://weather_user:YourPassword@cluster0.abcde.mongodb.net/weather_db?retryWrites=true&w=majority"
   ```

If your password contains special characters (`@`, `!`, `/`), you must URL-encode them:

```python
import urllib.parse
print(urllib.parse.quote_plus("YourPassword!"))
```

---

## Example Queries in MongoDB

Once data is ingested, open **MongoDB Atlas Data Explorer** or use the Mongo Shell.

### 1. Show 5 documents

```js
db.weather_data.find().limit(5).pretty()
```

### 2. Find data for a specific city

```js
db.weather_data.find({ city: "Nairobi" }).pretty()
```

### 3. Find records where temperature is above 25°C

```js
db.weather_data.find({ temp: { $gt: 25 } }).pretty()
```

### 4. Count records per city

```js
db.weather_data.aggregate([
  { $group: { _id: "$city", count: { $sum: 1 } } }
])
```

### 5. Average temperature per city

```js
db.weather_data.aggregate([
  { $group: { _id: "$city", avgTemp: { $avg: "$temp" } } }
])
```

---

## Troubleshooting

* **`ModuleNotFoundError: No module named 'kafka'`**
  → Run `pip install kafka-python` in your virtual environment.

* **`pymongo.errors.OperationFailure: bad auth`**
  → Double-check MongoDB Atlas username & password.
  → Ensure `/weather_db` is in the URI.
  → URL-encode your password.

* **Deprecation warnings for `datetime.utcnow()`**
  → Use:

  ```python
  from datetime import datetime, timezone
  datetime.now(timezone.utc)
  ```

---

## Future Improvements

* Containerize with Docker (Kafka + Zookeeper + Python).
* Add Flask API to serve recent weather data from MongoDB.
* Add Grafana dashboard for visualization.

---

## License

This project is licensed under the MIT License.

```

---

Would you like me to also generate a **diagram (architecture flow: OpenWeatherMap → Kafka → Consumer → MongoDB Atlas)** as part of the README, so it’s more visually clear?
```
