import json
import datetime
from collections import Iterable


DATETIME_FORMAT = '%d-%m-%Y %H:%M'

class SMS(object): 
    def __init__(self, sender, content): 
        assert isinstance(sender, str)
        assert isinstance(content, str)

        self.sender = sender
        self.content = content 

    @classmethod
    def from_json(cls, j): 
        if isinstance(j, str):
            j = json.loads(j)

        assert isinstance(j, dict)

        return cls(
            sender =j['from'],
            content=j['content']
        )

class Store(object):
    def __init__(self, name, address):
        assert isinstance(name,    str)
        assert isinstance(address, str) or address is None
        
        self.name = name
        self.address = address

    @classmethod
    def from_json(cls, j):
        if isinsatnce(j, str):
            j = json.loads(j)

        assert isinstance(j, dict) 
        
        return cls(
            name   =j['name'],
            address=j['address']
        )

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address
        }
        
class Payment(object): 
    def  __init__(self, type, amount, currency):
        if isinstance(type, str):
            type = type.lower()

        assert type in ("cash", "card") or type is None
        assert isinstance(amount, float)
        assert isinstance(currency, str) 
        
        self.type = type
        self.amount = amount
        self.currency = currency

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "currency": self.currency
        }
        

class Expense(object):
    def __init__(self, name, store, date_time, payment, category): 
        if isinstance(date_time, str):
            date_time = datetime.datetime.strptime(date_time, DATETIME_FORMAT)

        assert isinstance(name, str)
        assert isinstance(store, Store)
        assert isinstance(date_time, datetime.datetime)
        assert isinstance(payment, Payment) 
        assert isinstance(category, str)

        self.name = name 
        self.store = store 
        self.date_time = date_time
        self.payment = payment
        self.category = category

    @classmethod
    def from_json(cls, j):
        if isinstance(j, str):
            j = json.loads()

        assert isinstance(j, dict)

        return cls(
            name     =j['name'],
            store    =Store.from_json(j['store']),
            date_time=date_time,
            payment  =Payment.from_json(j['payment']),
            category =j['category']
        )

    def to_dict(self):
        return {
            'name':      self.name,
            'store':     self.store.to_dict(),
            'date_time': self.date_time.strftime(DATETIME_FORMAT),
            'payment':   self.payment.to_dict(),
            'category':  self.category
        }

class Sale(object): 
    def __init__(self, store, name, description, region, end, link): 
        if isinstance(end, str):
            end = datetime.datetime.strptime(end, DATETIME_FORMAT)

        assert isinstance(store, Store) 
        assert isinstance(name,        str)
        assert isinstance(description, str) 
        assert isinstance(region,      str)               or region is None 
        assert isinstance(end,         datetime.datetime) or end    is None
        assert isinstance(link,        str)               or link   is None

        self.store       = store
        self.name        = name
        self.description = description
        self.region      = region
        self.end         = end
        self.link        = link

    def to_dict(self):
        return {
            'store':       self.store.to_dict(),
            'name':        self.name,
            'description': self.description,
            'region':      self.region,
            'end':         self.end.strftime(DATETIME_FORMAT) if self.end is not None else None,
            'link':        self.link 
        }

class AnalyseResult(object):
    def __init__(self, expenses=tuple(), sales=tuple()): 
        assert isinstance(expenses, Iterable) and not isinstance(expenses, str)
        assert isinstance(sales,    Iterable) and not isinstance(sales,    str)

        assert all([isinstance(_, Expense) for _ in expenses])
        assert all([isinstance(_, Sale)    for _ in sales   ])
        
        self.expenses = list(expenses) 
        self.sales    = list(sales)

    def to_dict(self):
        return {
            'expenses': [expense.to_dict() for expense in self.expenses],
            'sales':    [sale   .to_dict() for sale    in self.sales   ]
        }

        
