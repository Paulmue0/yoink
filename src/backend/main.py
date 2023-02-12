from storage import Storage
from item import Request, Result
from enums import Condition
from storage import QueryType
from scraper import Scraper
from notifier import Notifier
from botservice import YoinkBotSender
from storage_chief import StorageChief
from servicecontroller import ServiceController
wishlist=[
Request(name='Nothing Phone 128GB', type=Condition.NEW, threshold=350),
Request(name='Nothing Phone 256GB', type=Condition.NEW, threshold=450),
Request(name='LG 38WN95c', type=Condition.NEW, threshold=950),
Request(name='Alienware AW3821DW', type=Condition.NEW, threshold=900),
Request(name='Alienware AW3423DWF', type=Condition.NEW, threshold=800),
Request(name='Alienware AW3423DW', type=Condition.NEW, threshold=800),
]


store = Storage()
chief = StorageChief(store)
sender = YoinkBotSender()
service_controller = ServiceController(sender)
scrape = Scraper(store, chief)
noti = Notifier(store, chief, service_controller)

for wish in wishlist:
    try:
        store.add(wish)
    except: continue
scrape.perform_scraping()
noti.send_all_notifications()
# scrap.perform_scraping()
store.save()


# telegram_bot = Notifier()
# telegram_bot.start_polling()
# telegram_bot.send_message("wie gehts")
# store.save()