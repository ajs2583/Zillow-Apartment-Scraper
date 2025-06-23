from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"

app = Flask(__name__)

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


def scrape_listings():
    response = requests.get(url=CLONE_URL, headers=HEADER)
    soup = BeautifulSoup(response.text, "html.parser")

    address_elements = soup.find_all('address', {"data-test": "property-card-addr"})
    addresses = [addr.get_text(strip=True).replace("|", "") for addr in address_elements]

    price_elements = soup.find_all('span', class_="PropertyCardWrapper__StyledPriceLine")
    prices = [
        price.get_text(strip=True).replace("+/mo", "").replace("/mo", "").replace("+ 1 bd", "").replace("+ 1bd", "")
        for price in price_elements
    ]

    address_links = soup.find_all('a', {"data-test": "property-card-link"})
    links = [link["href"] for link in address_links]

    listings = [dict(address=a, price=p, link=l) for a, p, l in zip(addresses, prices, links)]
    return listings


@app.route('/')
def index():
    listings = scrape_listings()
    return render_template('index.html', listings=listings)


if __name__ == '__main__':
    app.run(debug=True)
