import datetime

from pymongo import MongoClient


__db = MongoClient()['receipts_proj']
__reciepts = __db['receipts']

def add_receipt(receipt):
    if not 'date' in receipt:
        receipt['data'] = datetime.datetime.now().date()
        
    __reciepts.insert_one(receipt)

def get_all_receipts(): 
    return list(__reciepts.find({}, {'_id': False}))
