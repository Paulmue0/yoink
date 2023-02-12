from storage import Storage
from enums import QueryType, Condition
from item import Result
from copy import deepcopy
class StorageChief:
    def __init__(self, store:Storage) -> None:
        self.store =store
    def add_incoming_request(self, result:Result) -> None:
        associated_request = self.store.find_item_by_name(result.name, [QueryType.REQUESTS, result.type])
        if result.price is None:
            return
        if associated_request.threshold <= result.price:
            return
        if self.store.is_in_storage(result):
            old_result:Result = self.store.find_item_by_name(result.name, [QueryType.RESULTS, result.type])
            if old_result.price < result.price:
                return
            self.store.update(old_result, result)
        else:
            self.store.add(result)
    def messages_sent(self, type:Condition=Condition.NEW) -> None:
        results = self.store.get_data(QueryType.RESULTS)
        #New items
        products = results[type.value]
        for product in products:
            legacy_product = self.store.find_item_by_name(product['name'], [QueryType.RESULTS, type.value])
            updated_product = deepcopy(legacy_product)
            updated_product.sent = True
            self.store.update(legacy_product, updated_product)
        if type is Condition.NEW:
            self.messages_sent(Condition.OLD)


        