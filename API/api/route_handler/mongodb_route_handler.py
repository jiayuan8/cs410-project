from lib.mongo.connection import MongoConnection
import json 
from bson.json_util import dumps

def get_records_handler(request):
	json_data = json.loads(request.data)
	collection_name = json_data.get('collection',None)
	query = json_data.get('query',None)

	try:
		mongo = MongoConnection()
	except Exception as e:
		return {'error':e},400
	records_list = []
	try:
		if collection_name is not None and query is not None:

			records = mongo.db[collection_name].find(query)
			for rec in records:
				records_list.append(rec)

	except Exception as e:
		return {'error':e},400
	return {'records': json.loads(dumps(records_list))},200


def insert_records_handler(request):
	json_data = json.loads(request.data)
	collection_name = json_data.get('collection',None)
	records = json_data.get('records',None)
	
	try:
		mongo = MongoConnection()
	except:
		return {},400
	try:
		if collection_name is not None and records is not None:
			print(mongo.db[collection_name].insert_many(records))
	except Exception as e:
		return {'error':e},400
		
	return {},200

def delete_records_handler(request):
	json_data = json.loads(request.data)
	collection_name = json_data.get('collection',None)
	query = json_data.get('query',None)
	try:
		mongo = MongoConnection()
	except:
		return {},400
	try:
		if collection_name is not None and query is not None:
			mongo.db[collection_name].delete_many(query)
	except Exception as e:
		return {'error':e},400
	return {},200


	

