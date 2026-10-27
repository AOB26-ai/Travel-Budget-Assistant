import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY=os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_country_info(country_code):
    url=f"https://countries.dev/alpha/{country_code}"
    response = requests.get(url)
    if response == 200:
        return response.json()
    return None

def get_exchange_rates(base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Exchange rates received successfully")
        return data
    else:
        print(f"Failed to get exchange rates. Status code: {response.status_code}")
        return None

def convert_currency(amount, from_currency, rates_data):
    if not rates_data:
        print("No exchange rate data available.")
        return None

    if "base" not in rates_data or "rates" not in rates_data:
        print("Unexpected data format from exchange rate API:")
        print(rates_data)
        return None

    base = rates_data["base"]
    rates = rates_data["rates"]

    # Check if the currency the user entered is supported
    if from_currency != base and from_currency not in rates:
        print(f"Sorry, currency '{from_currency}' is not supported.")
        return None

    # Convert to base currency first
    if from_currency == base:
        amount_in_base = amount
    else:
        amount_in_base = amount / rates[from_currency]

    # Convert to KES, USD, EUR
    converted = {
        "USD": round(amount_in_base * (1 if base == "USD" else rates.get("USD", 0)), 2),
        "EUR": round(amount_in_base * rates.get("EUR", 0), 2),
        "KES": round(amount_in_base * rates.get("KES", 0), 2)
    }

    return converted


def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def run_tool():
    print("=" * 50)
    print("           TRAVEL BUDGET ASSISTANT")
    print("=" * 50)

    city = input("\nEnter destination city: ").strip()
    if not city:
        print("No city entered. Exiting.")
        return

    try:
        amount = float(input("How much money do you have? "))
    except ValueError:
        print("Please enter a valid number.")
        return
    from_currency = input("Currency of that money (e.g. USD, EUR, KES, GBP): ").strip().upper()
    if not from_currency:
        from_currency = "USD"
    

    print(f"\nFetching live data for {city.title()}...\n")

    # 1. Get weather
    weather_data = get_weather(city)
    if not weather_data:
        print(f"Could not find weather data for '{city}'.")
        return

    # 2. Get country info
    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)

    # 3. Get exchange rates
    rates_data = get_exchange_rates(base_currency="USD")
    if not rates_data:
        print("Could not fetch exchange rates.")
        return

    # Convert money
    print("Rates data:", rates_data)   
    converted = convert_currency(amount, from_currency, rates_data)

    # ========== DISPLAY RESULTS ==========
    print("=" * 50)
    print(f"  {city.title()}, {country_code}")
    print("=" * 50)

    # Weather
    print("\n🌤️  WEATHER")
    print(f"   Temperature : {weather_data['main']['temp']}°C")
    print(f"   Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"   Humidity    : {weather_data['main']['humidity']}%")
    print(f"   Wind        : {weather_data['wind']['speed']} m/s")

    # Country Info
    if country_data:
        print("\n🌍  COUNTRY INFO")
        print(f"   Region      : {country_data.get('region', 'Unknown')}")
        print(f"   Population  : {country_data.get('population', 'Unknown'):,}")
        currencies = country_data.get("currencies", [])
        currency_names = ", ".join([c.get("name", "") for c in currencies])
        print(f"   Currency    : {currency_names}")

    # Money Conversion
    print("\n💰  YOUR MONEY CONVERTED")
    print(f"   You have    : {amount:,.2f} {from_currency}")
    if converted:
        print(f"   ≈ {converted['KES']:,.2f} KES")
        print(f"   ≈ {converted['USD']:,.2f} USD")
        print(f"   ≈ {converted['EUR']:,.2f} EUR")
    else:
        print("   Could not convert. Check the currency code.")

    print("\n" + "=" * 50)

    # Optional: Save data
    all_data = {
        "city": city,
        "weather": weather_data,
        "country": country_data,
        "exchange_rates": rates_data,
        "converted_amounts": converted
    }
    save_to_file(all_data, f"{city.lower()}_travel_budget.json")

if __name__ == "__main__":
    run_tool()



