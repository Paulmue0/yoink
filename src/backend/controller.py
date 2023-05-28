from storage import Storage
from item import Request, Result
from enums import Condition
from storage import QueryType
from webscraper import WebScraper
from storage_chief import StorageChief
from notifier import Notifier
from message import Message
import time


class Controller:
    def __init__(self) -> None:
        self.store = Storage()
        self.chief = StorageChief(self.store)
        self.scrape = WebScraper(self.store, self.chief)
        self.notifyingService = Notifier(self.store, self.chief)

    def run(self):
        self.scrape.perform_scraping()
        self.store.save()

    def after_sent(self, chat_id):
        self.chief.messages_sent(chat_id)
        self.store.save()

    def pass_messages(self, chat_id) -> list[Message]:
        return self.notifyingService.get_all_unsent_messages(chat_id)

    def pass_chat_ids(self) -> list[str]:
        pass

    def pass_list_items(self):
        return self.chief.list_items()
