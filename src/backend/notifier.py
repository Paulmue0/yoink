from storage import Storage
from storage_chief import StorageChief
from enums import QueryType, Condition
from message import Message
from item import Result

class Notifier:
    def __init__(self, store:Storage, store_chief:StorageChief) -> None:
        self.store = store
        self.store_chief = store_chief

    def send_all_notifications(self, type:Condition=Condition.NEW):
        results = self.store.get_data(QueryType.RESULTS)
        products = results[type.value]
        for product in products:
            to_be_updated_item = self.store.find_item_by_name(product['name'], [QueryType.RESULTS, type.value])
            if not to_be_updated_item.sent:
                self.send_notification(to_be_updated_item)
        self.store_chief.messages_sent()
        if type is Condition.NEW:
            self.send_all_notifications(Condition.OLD)

    def send_notification(self, item:Result):
        self.service_controller.send(item.create_message())
    def get_all_unsent_messages(self, chat_id:str) -> list[Message]:
        results = self.store.get_data(QueryType.RESULTS)
        products = results[Condition.NEW.value]
        messages = []
        for product in products:
            to_be_updated_item: Result = self.store.find_item_by_name(product['name'], [QueryType.RESULTS, Condition.NEW.value])
            if not to_be_updated_item.sent:
                msg = Message(msg=to_be_updated_item.create_message())
                messages.append(msg)
        return messages
