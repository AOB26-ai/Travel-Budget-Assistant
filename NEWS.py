import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
country = "us"

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey=94feccff14714d47a14f9ec08bbb540f"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])

    print(f"\nFound {len(articles)} articles:\n")
    print("=" * 60)

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        source = article.get("source", {}).get("name", "Unknown")
        author = article.get("author", "Unknown")
        published = article.get("publishedAt", "")[:10]  # just the date
        url = article.get("url", "")

        print(f"{i}. {title}")
        print(f"   Source : {source}")
        print(f"   Author : {author}")
        print(f"   Date   : {published}")
        print(f"   Desc   : {description}")
        print(f"   Link   : {url}")
        print("-" * 60)

elif response.status_code == 401:
    print("API key is invalid or not yet active. Check your .env file.")
else:
    print(f"Error: {response.status_code}")