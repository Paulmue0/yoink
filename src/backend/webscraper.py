import requests
from bs4 import BeautifulSoup
from storage import Storage
from storage import QueryType
from item import *
from storage_chief import StorageChief
import time


class WebScraper:
    def __init__(self, store: Storage, chief: StorageChief) -> None:
        self.store = store
        self.chief = chief

    def get_price(self, url: str) -> float:
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        prices = doc.find_all("span", string="€")
        tile_container = doc.find_all("div", {"class": "tile-container"})
        if not tile_container:
            return
        best_tile_container = tile_container[0]

        price_container = best_tile_container.find("span", {"class": "price"})
        price_string = price_container.get_text()
        return self.format_price(price_string)

    def format_price(self, string: str) -> float:
        string = string.replace(".", "").replace(",", ".")
        price = ''.join(ch for ch in string if (ch.isdigit() | (ch == '.')))
        return float(price)

    def construct_query(self, name: str) -> str:
        query_name = name.lstrip().replace(" ", "+")
        return (f'https://www.billiger.de/search?searchstring={query_name}')

    def perform_scraping(self) -> None:
        items = self.store.get_data(QueryType.REQUESTS)
        # New Items
        for requested_product in items[Condition.NEW.value]:
            name = requested_product['name']
            search_query = self.construct_query(name)
            price = self.get_price(
                search_query)

            queried_product = Result(name=name, type=Condition.NEW, price=price, sent=False, url=search_query)

            if queried_product.price is not None:
                self.chief.add_incoming_result(queried_product)
                self.chief.add_to_price_history(name, price)
            time.sleep(5)
