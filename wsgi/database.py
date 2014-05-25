import os
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import json
DB_HOST=os.getenv('OPENSHIFT_MONGODB_DB_HOST', 'localhost')
DB_PORT=os.getenv('OPENSHIFT_MONGODB_DB_PORT', '27017')
client = MongoClient('mongodb://%s:%s/' % (DB_HOST, DB_PORT))
db = client['worldbank']
projects = db['projects']
procurements = db['procurements']
subscriptions = db['subscriptions']

def create_projects(projects_array):
	dict_projects_array = json.loads(projects_array)
	for project in dict_projects_array:
		projects.save(project)
		#TODO check if project got saved
	return projects_array

def get_all_projects():
	return '[' + ', '.join([json.dumps(result, default=json_util.default) for result in projects.find()]) + ']'

def create_procurement(procurement):
	dict_procurement = json.loads(procurement)
	dict_procurement['_id'] = dict_procurement['proc_id']
	existing_procurement = procurements.find_one({'_id':dict_procurement['proc_id']}, {'_id':0})
	if existing_procurement:
		return None
	ret = procurements.save(dict_procurement)
	if not ret:
		return None
	#TODO check if project got saved
	return procurement

def get_all_procurements():
	return '[' + ', '.join([json.dumps(result, default=json_util.default) for result in procurements.find()]) + ']'

def create_subscription(subscription):
	created = 0
	dict_subscription = json.loads(subscription)
	prev_subscription = subscriptions.find_one({'email': dict_subscription['email']})
	if prev_subscription:
		sid = prev_subscription.pop('_id')
		sectors = prev_subscription.get('sectors', [])
		locations = prev_subscription.get('locations', [])
		sectors.extend(dict_subscription.get('sectors'))
		locations.extend(dict_subscription.get('locations'))
		sectors = list(set(sectors))
		locations = list(set(locations))
		prev_subscription['sectors'] = sectors
		prev_subscription['locations'] = locations
		subscriptions.find_and_modify(query={'_id': sid}, 
					update={"$set": {"sectors": sectors, "locations": locations}})
		subscription = json.dumps(prev_subscription, default=json_util.default)
	else:
		subscriptions.save(dict_subscription)
		created = 1
	#TODO check if subscription got saved
	return subscription, created

def get_subscribers(procurement):
	subscribers = []
	resultset = projects.find({'id':procurement['projectid']}, {'sector':1})
	if not resultset or not resultset.count():
		return subscribers
	
	project = resultset[0]
	print 'PROJECT', project
	sectors = map(lambda x: x['Name'], project['sector'])		
	print 'SECTORS', sectors
	selected_subscribers = subscriptions.find({'sectors':{'$in' : sectors}}, {'email':1, '_id':0})
	print 'SELECTED_SUB', selected_subscribers
	return [email for email in set(map(lambda x: x['email'], selected_subscribers))]
	
	
