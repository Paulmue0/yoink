import json
from enum import Enum
from condition import Condition
from item import Item


class RequestResult(Enum):
    REQUESTS = 'Requests'
    RESULTS = 'Results'


class Storage:
    def __init__(self) -> None:
        self.store = {}
        self.init_store()

    def get_store(self):
        return self.store

    def get_data(self, req_res: RequestResult = None):
        return self.store[req_res.value]

    def add(self, item: Item, req_res: RequestResult):
        self.store[req_res.value][item.get_type()].append(item.dump())

    def update(self, item: Item, req_res: RequestResult):
        self.store[req_res.value][item.get_type()][self.indexOf(
            item, req_res)] = item.dump()

    def remove(self, item: Item, req_res: RequestResult):
        self.store[req_res.value][item.get_type()].remove(item.dump())

    def indexOf(self, item: Item, req_res: RequestResult):
        # return self.store[req_res.value][item.get_type()].index(item.get_name())
        return next((index for (index, d) in enumerate(self.store[req_res.value][item.get_type()]) if d["name"] == item.get_name()), None)

    def init_store(self):
        try:
            store = self.load()
        except:
            store = self.create_new_store()
        self.store = store

    def load(self):
        with open("./data/store.json", 'r') as f:
            store = json.load(f)
        return store

    def save(self):
        with open("./data/store.json", 'w') as f:
            json.dump(self.get_data(), f, indent=4)

    def create_new_store(self):
        store = {
            RequestResult.REQUESTS.value: {
                Condition.NEW.value: [],
                Condition.OLD.value: [],
            },
            RequestResult.RESULTS.value: {
                Condition.NEW.value: [],
                Condition.OLD.value: []
            },
        }
        return store
