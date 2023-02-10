from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from storage import Storage
from storage import QueryType
from item import *
from storage_chief import StorageChief
import time
import math


class Scraper:
    def __init__(self, store: Storage, store_chief:StorageChief) -> None:
        self.store = store
        self.store_chief = store_chief
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def get_price(self, product: Request) -> float:
        self.navigate_to_url(self.search_query(product))
        price_euros = self.get_element_by_xpath(
            '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[1]')
        price_cents = self.get_element_by_xpath(
            '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[3]')

        if price_euros is None or price_cents is None:
            return None

        price = self.element_to_price(price_euros, price_cents)

        return price

    def get_cheapest_offer_url(self, product: Item) -> str:
        self.navigate_to_url(self.search_query(product))
        cheapest_url = self.get_element_by_xpath(
            '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]')

        if cheapest_url is None:
            return None

        link = f"https://www.preissuchmaschine.de{cheapest_url.get_attribute('href')}"

        self.navigate_to_url(link)
        self.wait_for_url_change(link, 10)

        url = self.driver.current_url
        return str(url)

    def search_query(self, product: Item) -> str:
        query_name = product['name'].lstrip().replace(" ", "-")
        return (f'https://www.preissuchmaschine.de/Katalog/Suche/{query_name}.html')

    def navigate_to_url(self, url: str) -> None:
        self.driver.get(url)

    def get_element_by_xpath(self, xpath: str):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath))
            )
        except:
            self.driver.quit()
            return None
        return element

    def wait_for_url_change(self, url: str, seconds: int):
        try:
            result = WebDriverWait(self.driver, seconds).until(EC.url_changes(url))
        except:
            self.driver.quit()
        return result
        
    def element_to_price(self, integers, decimals) -> float:
        price = str(integers.text).replace(".", "")
        price += "."
        price += str(decimals.text)

        return float(price)

    def perform_scraping(self) -> None:
        # Perform scraping for NEW products
        items = self.store.get_data(QueryType.REQUESTS)
        for requested_product in items[Condition.NEW.value]:
            self.navigate_to_url(self.search_query(requested_product))

            queried_product = Result(name=requested_product['name'], type=Condition.NEW, price=self.get_price(
                requested_product), url=self.get_cheapest_offer_url(requested_product))

            if queried_product.price is not None:
                self.store_chief.add_incoming_request(queried_product)

            self.driver.quit()

        # Perform scraping for USED products
