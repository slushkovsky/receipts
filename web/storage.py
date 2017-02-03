import datetime
from pymongo import MongoClient

_db = MongoClient().checkstar

DATETIME_FORMAT = 'dd-MM-yyyy HH:mm'


class Storager(object):
    collection = None

    @classmethod
    def add(cls, user_id, obj):
        assert isinstance(obj, dict)

        if 'datetime' not in obj:
            obj['datetime'] = datetime.datetime.now().strftime(DATETIME_FORMAT)

        obj['user_id'] = user_id

        cls.collecion.inser_one(obj)

    @classmethod
    def get_all(cls, user_id):
        return list(cls.collection.find({'user_id': user_id},
                                        {'_id': False, 'user_id': False}))


class receipts(object):
    collection = _db.receipts


class expenses(object):
    collection = _db.expenses
