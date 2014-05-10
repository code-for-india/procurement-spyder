import urllib
import urllib2
import json
from bson import json_util
COUNT=5

def main():
	push_to_db(pull_from_worldbank())

def pull_from_worldbank():
	wb_url = 'http://search.worldbank.org/api/v2/projects'
	params = {
				'format':'json',
				'source':'IBRD',
				'countryname_exact':'Republic of India',
				'rows':COUNT,
				'geocode':'on',
				'kw':'N'
				}	
	data = urllib.urlencode(params)
	req = urllib2.Request(wb_url, data)
	response = urllib2.urlopen(req)
	projects_str = response.read()
	projects = json.loads(projects_str)
	projects_str = '[' + ', '.join([ json.dumps(project, default=json_util.default) for project in projects.get('projects').values()]) + ']'
	return projects_str

def push_to_db(projects):
	db_url = 'http://127.0.0.1:8000/projects'
	req = urllib2.Request(db_url, projects, {'Content-Type':'application/json'})
	response = urllib2.urlopen(req)
	print response.read()
		
if __name__ == '__main__':
	main()

