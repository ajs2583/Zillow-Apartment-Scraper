import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import requests

# ─── Config & Constants ────────────────────────────────────────────────────────
CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScMTs3orJel4v1R9Y2uw5cDErSjS9CbE2vO00dpXNU6RsdWXA/viewform?usp=header"
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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
response = requests.get(url=CLONE_URL, headers=HEADER)
soup = BeautifulSoup(response.text, "html.parser")

# SELENIUM SELECTORS
ADDRESS_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
)
PRICE_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
)
LINK_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
)


class ZillowHomeFinder:
    def __init__(self, soup):
        self.soup = soup

    def get_address(self):
        address_elements = soup.find_all('address', {"data-test": "property-card-addr"})
        return [addr.get_text(strip=True).replace("|", "") for addr in address_elements]

    def get_prices(self):
        price_elements = soup.find_all('span', class_="PropertyCardWrapper__StyledPriceLine")
        return [
            price.get_text(strip=True).replace("+/mo", "").replace("/mo", "").replace("+ 1 bd", "").replace("+ 1bd", "")
            for price
            in price_elements]

    def get_links(self):
        address_links = soup.find_all('a', {"data-test": "property-card-link"})
        return [link["href"] for link in address_links]

    def upload_data(self, url=FORM_URL):

        address_list = self.get_address()
        price_list = self.get_prices()
        link_list = self.get_links()

        driver.get(url)
        driver.maximize_window()
        time.sleep(1)

        try:
            address_input = wait.until(EC.presence_of_element_located(ADDRESS_INPUT_XPATH))
            price_input = wait.until(EC.presence_of_element_located(PRICE_INPUT_XPATH))
            link_input = wait.until(EC.presence_of_element_located(LINK_INPUT_XPATH))
            for address, price, link in zip(address_list, price_list, link_list):
                address_input.send_keys(address)
                price_input.send_keys(price)
                link_input.send_keys(link)
                link_input.send_keys(Keys.ENTER)
                time.sleep(1)
                address_input.clear()
                price_input.clear()
                link_input.clear()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error while uploading data: {e}")

        finally:
            driver.quit()


bot = ZillowHomeFinder(soup)
bot.upload_data()
