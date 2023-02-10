from enum import Enum

class QueryType(Enum):
    REQUESTS = 'REQUESTS'
    RESULTS = 'RESULTS'

class Condition(Enum):
    NEW = 'NEW'
    OLD = 'OLD'
