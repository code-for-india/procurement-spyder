from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['database_name']
collection = db['collection_name']

# Create index of candidates collection
collection.create_index([("field1", ASCENDING),
                         ("field2", ASCENDING),
                         ("field3", DESCENDING)])

PAGE_LIMIT = 20


#
# Get One or More documents
#
def get(id=None, query=None, page=1, limit=PAGE_LIMIT):

  # Only one entry
  if id:
    result = collection.find_one({'_id': ObjectId(_id)})
    return json.dumps(result, default=json_util.default)

  # Multiple entries
  json_docs = []
  resultset = collection.find(query, skip=(page-1)*limit, limit=limit)
  for result in resultset:
      result_json = json.dumps(result, default=json_util.default)
      json_docs.append(result_json)

  return json_docs;


#
# Create document
#
def create(document):
  return collection.save(document)

#
# Find document by query and Update document by data
#
def update(query=None, data={}):
  if query:
    collection.find_and_modify(query=query, update={"$set": data })
  else:
    print "Query is missing. Could not update document."

#
# Remove one or more documents
#
def remove(query=None):
  if query:
    collection.remove(query)
  else:
    print "Query is missing. Could not remove document."
