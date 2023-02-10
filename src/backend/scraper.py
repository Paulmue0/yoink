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
import time
import math


class Scraper:
    def __init__(self, store: Storage) -> None:
        self.store = store
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def get_price(self, product: Request) -> float:
        self.set_driver_path(self.search_query(product))
        try:
            price_euros = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[1]'))
            )
        except:
            self.driver.quit()
            return math.inf

        try:
            price_cents = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[3]'))
            )
        except:
            self.driver.quit()
            return math.inf
        price = str(price_euros.text).replace(".", "")
        price += "."
        price += str(price_cents.text)
        print(f"Der Preis ist heiß: nur {price}€uronen\n")
        return float(price)

    def get_cheapest_offer_url(self, product: Item) -> str:
        self.set_driver_path(self.search_query(product))
        try:
            cheapest_url = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]'))
            )
        except:
            self.driver.quit()
            return ''
        link = f"https://www.preissuchmaschine.de{cheapest_url.get_attribute('href')}"
        try:
            self.driver.get(link)
        except:
            return ''
        try:
            definitive_url = WebDriverWait(self.driver, 10).until(EC.url_changes(link))
        except:
            self.driver.quit()
            return ''
        
        url = self.driver.current_url
        return str(url)

    def search_query(self, product: Item) -> str:
        query_name = product['name'].lstrip().replace(" ", "-")
        return (f'https://www.preissuchmaschine.de/Katalog/Suche/{query_name}.html')

    def set_driver_path(self, url):
        self.driver.get(url)

    def perform_scraping(self) -> None:
        # Perform scraping for NEW products
        items = self.store.get_data(QueryType.REQUESTS)
        for requested_product in items[Condition.NEW.value]:
            self.set_driver_path(self.search_query(requested_product))

            queried_product = Result(name=requested_product['name'], type=Condition.NEW, price=self.get_price(
                requested_product), url=self.get_cheapest_offer_url(requested_product))
            
            if queried_product.price <= requested_product['threshold']:
                self.store.add(queried_product)

            self.driver.quit()

        # Perform scraping for USED products
