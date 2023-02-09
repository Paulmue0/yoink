from storage import Storage
from item import Request
from condition import Condition
from storage import RequestResult
from scraper import Scraper

new_item = Request('LG 38WN95c', Condition.NEW, 400)
second_item = Request('LG 38WN959c', Condition.NEW, 900)

store = Storage()

scrape = Scraper(store)
scrape.perform_scraping()

