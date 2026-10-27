import requests
url = "https://countries.dev/name/nigeria"
response = requests.get(url)
print("Status Code:", response.status_code)
print("Data received:", response.json())

if response.status_code == 200:
    data = response.json()
    country = data[0]

    name = country["name"]
    capital = country["capital"]
    population = country["population"]
    currency = country["currencies"][0]["code"]

    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population:,}")
    print(f"Currency: {currency}")
else:
    print("Request failed. Status:", response.status_code)