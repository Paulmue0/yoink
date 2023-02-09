from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from storage import Storage
from storage import RequestResult
from item import *
import time


class Scraper:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def get_price(self, product: Request) -> float:
        self.set_driver_path(self.search_query(product['name']))
        try:
            price_euros = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[1]'))
            )
        except:
            self.driver.quit()

        try:
            price_cents = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/span/span[3]'))
            )
        except:
            self.driver.quit()
        print(f"Der Preis ist heiß: nur {price_euros.text},{price_cents.text}\n")
        return f"{price_euros.text},{price_cents.text}"

    def get_cheapest_offer_url(self, product: Item) -> str:
        self.set_driver_path(self.search_query(product['name']))
        try:
            cheapest_url = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]'))
            )
        except:
            self.driver.quit()
        # self.driver.find_element(By.XPATH('/html/body/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]')).click();
        # cheapest_url.click()
        link = f"https://www.preissuchmaschine.de{cheapest_url.get_attribute('href')}"
        self.driver.get(link)
        time.sleep(3)
        url = self.driver.current_url
        # print(cheapest_url)
        # print(link)
        print(url)

    def search_query(self, product: Item) -> str:
        query_name = product.lstrip().replace(" ", "-")
        return (f'https://www.preissuchmaschine.de/Katalog/Suche/{query_name}.html')

    def set_driver_path(self, url):
        self.driver.get(url)

    def perform_scraping(self) -> None:
        # Perform scraping for NEW products
        items = self.storage.get_data(RequestResult.REQUESTS)
        for product in items[Condition.NEW.value]:
            self.set_driver_path(self.search_query(product['name']))

            queried_product = Result(product['name'], Condition.NEW, self.get_price(
                product), False, self.get_cheapest_offer_url(product))

            self.driver.quit()

        # Perform scraping for USED products
