from storage import Storage
from item import Request, Result
from enums import Condition
from storage import QueryType
from scraper import Scraper
from notifier import Notifier
from botservice import YoinkBotSender
from storage_chief import StorageChief
from servicecontroller import ServiceController

first_item = Request(name='Nothing Phone', type=Condition.NEW, threshold=500)
first_result = Result(name='Nothing Phone', type=Condition.NEW, price=400, url="paulpelikan.de")
second_item = Request(name='LG 38WN959c', type=Condition.NEW, threshold=900)

store = Storage()
chief = StorageChief(store)
sender = YoinkBotSender()
service_controller = ServiceController(sender)
noti = Notifier(store, chief, service_controller)
noti.send_all_notifications()
# scrap.perform_scraping()
store.save()


# telegram_bot = Notifier()
# telegram_bot.start_polling()
# telegram_bot.send_message("wie gehts")
# store.save()