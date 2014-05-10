from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['worldbank']
projects = db['projects']

def create_projects(projects_array):
	dict_projects_array = json.loads(projects_array)
	for project in dict_projects_array: 
		projects.save(project)
		#TODO check if project got saved
	return projects_array

def get_all_projects():
	return '[' + ', '.join([json.dumps(result, default=json_util.default) for result in projects.find()]) + ']'

	
	 
