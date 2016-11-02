from pymongo import MongoClient


__db = MongoClient()['receipts_proj']
__reciepts = __db['receipts']

def add_receipt(receipt): 
	__reciepts.insert_one(receipt)

def get_all_receipts(): 
	return list(__reciepts.find({}, {'_id': False}))