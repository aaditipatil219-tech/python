from flask import Flask, request, render_template_string
import urllib.request
import urllib.parse
import urllib.error
import json
import time

app = Flask(__name__)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WeatherNow</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dce8ff, #e6f8f4);
            color: #1c2940;
            min-height: 100vh;
            padding: 40px 15px;
        }

        .container {
            max-width: 720px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 35px;
        }

        h1 {
            font-size: 38px;
            margin-bottom: 10px;
        }

        header p { color: #64748b; }

        form {
            display: flex;
            gap: 10px;
            padding: 12px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 30px #263c6015;
        }

        input {
            flex: 1;
            min-width: 0;
            border: none;
            outline: none;
            padding: 12px;
            font-size: 16px;
        }

        button {
            border: none;
            border-radius: 10px;
            padding: 12px 18px;
            background: #3867e8;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover { background: #244dc4; }

        .card {
            margin-top: 25px;
            padding: 28px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 12px 40px #263c6015;
        }

        .location { color: #64748b; }

        .temperature {
            font-size: 64px;
            font-weight: bold;
            margin: 15px 0 5px;
        }

        .condition {
            font-size: 19px;
            color: #64748b;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 25px;
        }

        .metric {
            background: #f4f7fc;
            padding: 18px;
            border-radius: 12px;
        }

        .metric p {
            color: #64748b;
            margin: 0 0 8px;
        }

        .metric strong { font-size: 20px; }

        .error {
            margin-top: 20px;
            padding: 16px;
            background: #fff0ef;
            color: #a52d2d;
            border-radius: 12px;
        }

        footer {
            text-align: center;
            color: #64748b;
            font-size: 12px;
            margin-top: 25px;
        }

        @media (max-width: 480px) {
            body { padding: 25px 12px; }
            h1 { font-size: 30px; }
            form { flex-wrap: wrap; }
            input { width: 100%; }
            button { width: 100%; }
            .grid { grid-template-columns: 1fr 1fr; }
            .card { padding: 20px; }
        }
    </style>
</head>

<body>
<div class="container">
    <header>
        <h1>☀️ WeatherNow</h1>
        <p>Live weather reports for cities around the world</p>
    </header>

    <form method="POST">
        <input
            type="text"
            name="city"
            placeholder="Enter city, e.g. Bengaluru"
            value="{{ city }}"
            required
        >
        <button type="submit">Search Weather</button>
    </form>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    {% if weather %}
    <section class="card">
        <div class="location">CURRENT WEATHER</div>
        <h2>{{ weather.location }}</h2>
        <div class="temperature">{{ weather.temperature }}°C</div>
        <div class="condition">{{ weather.condition }}</div>

        <div class="grid">
            <div class="metric">
                <p>🌡️ Feels like</p>
                <strong>{{ weather.feels }}°C</strong>
            </div>
            <div class="metric">
                <p>💧 Humidity</p>
                <strong>{{ weather.humidity }}%</strong>
            </div>
            <div class="metric">
                <p>💨 Wind speed</p>
                <strong>{{ weather.wind }} km/h</strong>
            </div>
            <div class="metric">
                <p>🌧️ Precipitation</p>
                <strong>{{ weather.rain }} mm</strong>
            </div>
        </div>

        <p class="location">Local time: {{ weather.time }}</p>
    </section>
    {% endif %}

    <footer>Weather data by Open-Meteo · Built with Flask, HTML and CSS</footer>
</div>
</body>
</html>
"""

CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}


def api_get(url, params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url + "?" + query,
        headers={"User-Agent": "WeatherNow/1.0"}
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as error:
            if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(attempt + 1)
                continue
            raise

        except urllib.error.URLError:
            if attempt < 2:
                time.sleep(attempt + 1)
                continue
            raise


def get_weather(city):
    places = api_get(GEOCODING_URL, {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }).get("results", [])

    if not places:
        return None

    place = places[0]

    data = api_get(WEATHER_URL, {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,"
            "weather_code,wind_speed_10m"
        ),
        "timezone": "auto"
    })

    current = data["current"]

    location = place["name"]
    if place.get("admin1"):
        location += ", " + place["admin1"]
    if place.get("country"):
        location += ", " + place["country"]

    return {
        "location": location,
        "temperature": current["temperature_2m"],
        "feels": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "rain": current["precipitation"],
        "condition": CODES.get(
            current["weather_code"], "Unknown conditions"
        ),
        "time": current.get("time", "Unavailable").replace("T", " ")
    }


@app.route("/", methods=["GET", "POST"])
def home():
    city = request.form.get("city", "").strip()
    weather = None
    error = None

    if city:
        try:
            weather = get_weather(city)
            if weather is None:
                error = "City not found. Please check the spelling."

        except urllib.error.HTTPError as exc:
            error = (
                "The weather service is temporarily unavailable."
                if exc.code in (429, 500, 502, 503, 504)
                else f"Weather API error: HTTP {exc.code}"
            )

        except (urllib.error.URLError, TimeoutError):
            error = "Connection failed. Check your internet and try again."

        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            error = "Could not read weather data. Please try again."

    return render_template_string(
        HTML, city=city, weather=weather, error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
    