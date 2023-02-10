import json

from item import Item
import os
from enums import QueryType, Condition




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
            print(f"get_dataError: RequestResult value '{query_type.value}' not found in the store.")
            return None

    def add(self, item: Item):
        index = self.indexOf(item)
        if index is None:
            try:
                self.store[item.verbose_query_type()][item.type].append(item.dump())
            except KeyError:
                print(f"AddError: Item type '{item.type}' not found in the store for RequestResult value '{item.verbose_query_type()}'.")
        else:
            raise ValueError("AddError: Item already exists in the store.")
        

    def update(self, old_item: Item, new_item: Item):
        if self.is_in_storage(old_item) and not self.is_in_storage(new_item):
            try:
                self.remove(old_item)
                self.add(new_item)
            except KeyError:
                print(f"UpdateError: Item type '{old_item.type}' not found in the store for RequestResult value '{old_item.verbose_query_type()}'.")
        else:
            print(f"UpdateError: Item with name '{old_item.name}' not found in the store for RequestResult value '{old_item.verbose_query_type()}'.")

    def remove(self, item: Item):
        if self.is_in_storage(item):
            try:
                self.store[item.verbose_query_type()][item.type].remove(item.dump())
            except KeyError:
                print(f"RemoveError: Item type '{item.type}' not found in the store for RequestResult value '{item.verbose_query_type()}'.")
        else:
            print(f"RemoveError: Item with name '{item.name}' not found in the store for RequestResult value '{item.verbose_query_type()}'.")

    def indexOf(self, item: Item):
        try:
            return next((index for (index, d) in enumerate(self.store[item.verbose_query_type()][item.type]) if d["name"] == item.name), None)
        except KeyError:
            print(f"IndexFindError: Item type '{item.type}' not found in the store for RequestResult value '{item.verbose_query_type()}'.")
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