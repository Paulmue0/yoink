import requests
from bs4 import BeautifulSoup
from storage import Storage
from storage import QueryType
from item import *
from storage_chief import StorageChief
import time

class WebScraper:
    def __init__(self, store:Storage, chief:StorageChief) -> None:
        self.store = store
        self.chief = chief

    def get_price(self, url:str) -> float:
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        # r=html=s.get(url).text
        prices = doc.find_all("span", string="€")
        tile_container = doc.find_all("div", {"class": "tile-container"})
        if not tile_container:
            return
        best_tile_container = tile_container[0]


        price_container = best_tile_container.find("span", {"class": "price"})   
        price_string = price_container.get_text()
        return self.format_price(price_string)
    def format_price(self, string:str) -> float:
        string = string.replace(".", "").replace(",", ".")
        price = ''.join(ch for ch in string if (ch.isdigit() | (ch == '.')))
        return float(price)
    def construct_query(self, name:str) -> str:
        query_name = name.lstrip().replace(" ", "+")
        return (f'https://www.billiger.de/search?searchstring={query_name}')
    def perform_scraping(self) -> None:
        items = self.store.get_data(QueryType.REQUESTS)
        # New Items
        for requested_product in items[Condition.NEW.value]:
            search_query = self.construct_query(requested_product['name'])

            queried_product = Result(name=requested_product['name'], type=Condition.NEW, price=self.get_price(
                search_query), sent=False, url=search_query)

            if queried_product.price is not None:
                self.chief.add_incoming_request(queried_product)
            time.sleep(5)