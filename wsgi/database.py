from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import json

client = MongoClient('mongodb://localhost:27017/')
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
	existing_procurement = procurements.find_one({'_id':dict_procurement['proc_id']})
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
	dict_form_data = json.loads(subscription)
	subscriptions.save(dict_form_data)
	#TODO check if subscription got saved
	return subscription

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
	
	
