from condition import Condition

class Item:
    def __init__(self, name, type:Condition) -> None:
        self.name = name
        self.type = type.value

    def get_name(self) -> str:
        return self.name

    def get_type(self):
        return self.type

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type
    def dump(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(value)}


class Request(Item):
    def __init__(self, name, type, threshold: float) -> None:
        super().__init__(name, type)
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold: float):
        self.threshold = threshold
    def dump(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(value)}



class Result(Item):
    def __init__(self, name, type, price: float, sent: bool, url) -> None:
        super().__init__(name, type)
        self.price = price
        self.sent = sent
        self.url = url

    def get_price(self):
        return self.price

    def get_sent(self):
        return self.sent

    def get_url(self):
        return self.url

    def set_price(self, price: float):
        self.price = price

    def set_sent(self, sent: bool):
        self.sent = sent

    def set_url(self, url: float):
        self.url = url

    def create_link():
        pass

