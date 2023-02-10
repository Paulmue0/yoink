from storage import Storage
from item import Request, Result
from enums import Condition
from storage import QueryType
from scraper import Scraper
from notifier import Notifier

first_item = Request(name='Nothing Phone', type=Condition.NEW, threshold=500)
second_item = Request(name='LG 38WN959c', type=Condition.NEW, threshold=900)

store = Storage()
# scrap = Scraper(store)
# scrap.perform_scraping()
# store.save()


telegram_bot = Notifier()
# telegram_bot.start_polling()
# telegram_bot.send_message("wie gehts")
# store.save()