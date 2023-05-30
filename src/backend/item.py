from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enums import Condition, QueryType
from message import Message


@dataclass()
class Item(ABC):
    name: str
    _name: str = field(init=False, repr=False)
    type: Condition
    _type: Condition = field(init=False, repr=False)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Condition:
        return self._type

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @type.setter
    def type(self, condition: Condition) -> None:
        self._type = condition.value

    def exclude_private(self, vars: dict) -> dict:
        return {key: value for key, value in vars.items() if not key.startswith('_')}

    def dump(self) -> dict:
        vars = asdict(self)
        return self.exclude_private(vars)

    @abstractmethod
    def query_type(self, verbose: bool = True):
        """returns the querytiype of the class as a string"""


@dataclass()
class Request(Item):
    threshold: float
    _threshold: float = field(init=False, repr=False)
    price_history: list = field(default_factory=list) 

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: float) -> None:
        self._threshold = threshold

    def query_type(self, verbose: bool = True):
        if verbose:
            return QueryType.REQUESTS.value
        return QueryType.REQUESTS


@dataclass()
class Result(Item):
    price: float
    _price: float = field(init=False, repr=False)
    sent: bool = False
    _sent: bool = field(init=False, repr=False)
    url: str
    _url: str = field(init=False, repr=False)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        self._price = price

    @property
    def sent(self) -> bool:
        return self._sent

    @sent.setter
    def sent(self, sent: bool) -> None:
        self._sent = sent

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    def create_message(self):
        return f"Preisdrop für \"{self.name}\"\nGefundener Preis: {self.price}€\n\nDu findest das Angebot hier:\n{self.url}"

    def query_type(self, verbose: bool = True):
        if verbose:
            return QueryType.RESULTS.value
        return QueryType.RESULTS


def create_item_from_dict(obj: dict, properties: list[QueryType, Condition]) -> Item:
    if properties[0] == QueryType.REQUESTS:
        return Request(name=obj['name'], type=properties[1], threshold=obj['threshold'], price_history= obj['price_history'])
    if properties[0] == QueryType.RESULTS:
        return Result(name=obj['name'], type=properties[1], price=obj['price'], sent=(obj['sent']), url=obj['url'])
