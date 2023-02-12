import json

from item import Item, create_item_from_dict
import os
from enums import QueryType, Condition
import traceback


class Storage:
    def __init__(self) -> None:
        self.store = {}
        self.init_store()

    def is_in_storage(self, item) -> bool:
        index = self.indexOf(item)
        if index is None:
            return False
        return True

    def get_store(self):
        return self.store

    def get_data(self, query_type: QueryType = None):
        try:
            return self.store[query_type.value]
        except KeyError:
            print(
                f"get_dataError: RequestResult value '{query_type.value}' not found in the store.")
            return None

    def find_item_by_name(self, name: str, search_space: list[QueryType, Condition]) -> Item:
        try:
            result = [d for d in self.store[search_space[0].value]
                      [search_space[1]] if d["name"] == name][0]
            return create_item_from_dict(result, [search_space[0], Condition(search_space[1])])
        except KeyError:
            print(traceback.format_exc())
            print(KeyError.with_traceback)
            # print(f"FindError: Item with type '{item.type}' not found in the store for search_space value '{search_space}'.")
            return None

    def add(self, item: Item) -> None:
        index = self.indexOf(item)
        if index is None:
            try:
                self.store[item.query_type()][item.type].append(item.dump())
            except KeyError:
                print(
                    f"AddError: Item type '{item.type}' not found in the store for RequestResult value '{item.query_type()}'.")
        else:
            raise ValueError("AddError: Item already exists in the store.")

    def update(self, old_item: Item, new_item: Item) -> None:
        if self.is_in_storage(old_item) and not self.is_in_storage(new_item):
            try:
                self.remove(old_item)
                self.add(new_item)
            except KeyError:
                print(
                    f"UpdateError: Item type '{old_item.type}' not found in the store for RequestResult value '{old_item.query_type()}'.")
        else:
            print(f"UpdateError: The item to be updated is not in the store.")

    def remove(self, item: Item):
        if self.is_in_storage(item):
            try:
                self.store[item.query_type()][item.type].remove(item.dump())
            except KeyError:
                print(
                    f"RemoveError: Item type '{item.type}' not found in the store for RequestResult value '{item.query_type()}'.")
        else:
            print(
                f"RemoveError: Item with name '{item.name}' not found in the store for RequestResult value '{item.query_type()}'.")

    def indexOf(self, item: Item) -> int:
        try:
            if item.query_type(verbose=False) == QueryType.REQUESTS:
                return next((index for (index, d) in enumerate(self.store[item.query_type()][item.type])
                             if
                             d["name"] == item.name
                             and d["threshold"] == item.threshold
                             and d["type"] == item.type), None)
            elif item.query_type(verbose=False) == QueryType.RESULTS:
                return next((index for (index, d) in enumerate(self.store[item.query_type()][item.type])
                             if
                             d["name"] == item.name and
                             d["type"] == item.type and
                             d["price"] == item.price and
                             (d["sent"] == 'true') == item.sent
                             and d["url"] == item.url), None)

        except KeyError:
            print(
                f"IndexFindError: Item type '{item.type}' not found in the store for RequestResult value '{item.query_type()}'.")
            return None

    def init_store(self):
        if os.path.exists("./data/store.json"):
            self.store = self.load()
        else:
            self.store = self.create_new_store()

    def load(self):
        try:
            with open("./data/store.json", 'r') as f:
                store = json.load(f)
            return store
        except FileNotFoundError:
            print(f"LoadingError: The Store was not found at './data/store.json'")

    def save(self):
        with open("./data/store.json", 'w') as f:
            json.dump(self.get_store(), f, indent=4)

    def create_new_store(self):
        store = {
            QueryType.REQUESTS.value: {
                Condition.NEW.value: [],
                Condition.OLD.value: [],
            },
            QueryType.RESULTS.value: {
                Condition.NEW.value: [],
                Condition.OLD.value: []
            },
        }
        return store
