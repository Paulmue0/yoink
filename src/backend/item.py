from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enums import Condition, QueryType
from message import Message

@dataclass(kw_only=True)
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
    def verbose_query_type(self) -> str:
        """returns the querytiype of the class as a string"""

@dataclass(kw_only=True)
class Request(Item):
    threshold: float
    _threshold: float = field(init=False, repr=False)

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: float) -> None:
        self._threshold = threshold
    def verbose_query_type(self) -> str:
        return QueryType.REQUESTS.value


@dataclass(kw_only=True)
class Result(Item):
    price: float
    _price: float = field(init=False, repr=False)
    sent: bool = False
    _sent: bool = field(init=False, repr=False, default_factory=bool)
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
        return Message(msg= f"Preisdrop für *{self.name}*\nGefundener Preis: {self.price}€\n\nDu findest das Angebot hier:\n{self.url}")
    def verbose_query_type(self) -> str:
        return QueryType.RESULTS.value
