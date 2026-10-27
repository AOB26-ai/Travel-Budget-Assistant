import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 0.28,        # Kakamega
    "longitude": 34.75,
    "current_weather": True
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Data received:")
    print(data)

    weather = data.get("current_weather", {})
    temperature = weather.get("temperature")
    wind_speed = weather.get("windspeed")
    wind_direction = weather.get("winddirection")
    print(f"Weather Data for Kakamega:")
    print(f"Temperature: {temperature}")
    print(f"Wind Speed: {wind_speed}")
    print(f"Wind Direction: {wind_direction}")
else:
    print("Request failed")