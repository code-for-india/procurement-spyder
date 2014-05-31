import os
from datetime import datetime
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import json
import mailer
import states

DB_URL = os.getenv('OPENSHIFT_MONGODB_DB_URL', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('OPENSHIFT_APP_NAME', 'worldbank')
client = MongoClient('%s%s' % (DB_URL, DB_NAME))
db = client[DB_NAME]
projects = db['projects']
procurements = db['procurements']
subscriptions = db['subscriptions']

def save_project(project):
	existing_project = projects.find_one({'id': project['id']})
	if existing_project:
		return None
	projects.save(project)
	return project

def get_all_projects():
	return '[' + ', '.join([json.dumps(result, default=json_util.default) for result in projects.find()]) + ']'

def save_procurement(procurement):
	existing_procurement = procurements.find_one({'_id': procurement['proc_id']})
	if existing_procurement:
		return None
	procurements.save(procurement)
	subscribers = get_subscribers(procurement)
	print 'SUBSCRIBERS-------------', subscribers
	if subscribers:
		mailer.send_subscription_mail(subscribers, procurement)
	return procurement

def get_all_procurements():
	return '[' + ', '.join([json.dumps(result, default=json_util.default) for result in procurements.find()]) + ']'

def create_subscription(dict_subscription):
	created = 0

	prev_subscription = subscriptions.find_one({'email': dict_subscription['email']})
	timenow = str(datetime.utcnow())
	if prev_subscription:
		s_id = prev_subscription.pop('_id')
		sectors = prev_subscription.get('sectors', [])
		locations = prev_subscription.get('locations', [])
		sectors.extend(dict_subscription.get('sectors'))
		locations.extend(dict_subscription.get('locations'))
		sectors = list(set(sectors))
		locations = list(set(locations))
		prev_subscription['sectors'] = sectors
		prev_subscription['locations'] = locations
		prev_subscription['updated_at'] = timenow
		subscriptions.find_and_modify(query={'_id': s_id},
					update={"$set": {"sectors": sectors, 
							 "locations": locations, 
							 "updated_at": timenow}
						})
		prev_subscription['updated'] = True		
		subscription = json.dumps(prev_subscription, default=json_util.default)
	else:
		dict_subscription['created_at'] = timenow
		dict_subscription['verified'] = False
		s_id = subscriptions.save(dict_subscription)
		created = 1
		subscription = json.dumps(dict_subscription, default=json_util.default)
	return subscription, created, s_id

def delete_subscription(subscription_id):
	return subscriptions.find_and_modify(query={'_id': ObjectId(subscription_id)}, remove=True)

def get_query(sectors, location):
	query = {}
	query['$and'] = [{'locations': {'$in': [location, 'All over India']}}, 
			 {'sectors': {'$in': sectors}},
			 {'verified': True}]
	return query

def get_subscribers(procurement):
	subscribers = []
	resultset = projects.find({'id':procurement['projectid']}, {'sector':1})
	if not resultset or not resultset.count():
		return subscribers

	project = resultset[0]
	print 'PROJECT', project
	sectors = map(lambda x: x['Name'], project['sector'])
	print 'SECTORS', sectors
	state = states.get_state(procurement['city'])
	if not state:
		return subscribers 
	query = get_query(sectors, state)
	print 'QUERY', query
	selected_subscribers = subscriptions.find(query, {'email':1, '_id':0})
	print 'SELECTED_SUB', selected_subscribers
	return [email for email in set(map(lambda x: x['email'], selected_subscribers))]

def verify_subscription(token):
	subscription = subscriptions.find_and_modify(
				query={'_id': ObjectId(token)},
				update={"$set": {"verified": True}})
	return subscription
