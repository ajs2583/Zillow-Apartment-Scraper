from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/"
ZILLOW_BASE = "https://www.zillow.com/homes/for_rent/"

app = Flask(__name__)


def build_url(city: str | None) -> str:
    """Return a Zillow search URL for the given city."""
    if not city:
        return ZILLOW_URL
    city_path = city.strip().replace(" ", "-")
    return f"{ZILLOW_BASE}{city_path}_rb/"


def _price_to_int(price: str | None) -> int | None:
    """Convert a price string like '$2,500/mo' to an integer."""
    if not price:
        return None
    import re

    digits = re.findall(r"\d+", price.replace(",", ""))
    if not digits:
        return None
    return int("".join(digits))

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}


def scrape_listings(city: str | None = None):
    """Scrape listing data from Zillow search results."""

    url = build_url(city)
    response = requests.get(url=url, headers=HEADER)
    soup = BeautifulSoup(response.text, "html.parser")

    data_script = soup.find("script", id="__NEXT_DATA__", type="application/json")
    listings = []
    if not data_script:
        return listings

    try:
        import json

        data = json.loads(data_script.string)
        results = (
            data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
        )
        for item in results:
            address = item.get("address")
            # Pull the price from the json. Some results use a nested
            # `units` list while others expose `unformattedPrice` or
            # `price`. We try all options so that the value is populated.
            price = (
                item.get("price")
                or item.get("unformattedPrice")
                or (item.get("units") or [{}])[0].get("price")
            )
            link = item.get("detailUrl")
            if link and link.startswith("/"):
                link = f"https://www.zillow.com{link}"
            listings.append({"address": address, "price": price, "link": link})
    except Exception:
        # fail silently if page structure changes
        return []

    return listings


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/listings')
def index():
    city = request.args.get('city')
    max_price = request.args.get('max_price', type=int)

    listings = scrape_listings(city)

    if max_price is not None:
        listings = [
            l for l in listings
            if (_price_to_int(l.get('price')) or 0) <= max_price
        ]

    return render_template(
        'index.html',
        listings=listings,
        city=city,
        max_price=max_price,
    )


if __name__ == '__main__':
    app.run(debug=True)
