import os
import tempfile
import urllib
import urllib2
import urlparse
import json
from bson import json_util
from BeautifulSoup import BeautifulSoup

COUNT=200

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

'''
def pull_procurements():
	wb_url = 'http://www.worldbank.org/p2e/generateexcel.html'
	params = {
				'noOfRows':COUNT,
				'startIndex':0,
				'lang':'en',
				'notice_type_exact':'',
				'procurement_method_name_exact':'',
				'procurement_type_exact':'',
				'project_ctry_name_exact':'',
				'regionname_exact':'',
				'project_ctry_code_exact':'IN',
				'procurement_method_code_exact':'',
				'project_id':'',
				'sectorcode_exact':'',
				'showrecent':'',
				'searchString':'',
				'option':'noticesearchresult'
			}
	proc_file = os.path.join(tempfile.gettempdir(), 't.xls')
	try:
		os.remove(proc_file)
	except OSError, e:
		pass

	start_index = 1

	while True:
		data = urllib.urlencode(params)
		print wb_url+'?'+data
		req = urllib2.Request(wb_url, data)
		response = urllib2.urlopen(req)
		f = open(proc_file, 'ab')
		buf = response.read()
		if not buf:
			break
		f.write(buf)
		f.close()
		start_index = start_index + COUNT
		params['startIndex'] = start_index;
	return proc_file
'''

def pull_procurements():
	url = 'http://www.worldbank.org/p2e/procurement/procurementsearchpagination.html'
	params = {
				'procurement_method_name_exact': '', 
				'submission_strdate': '', 
				'notice_type_exact': '', 
				'activeStartIndex': 0, 
				'noOfRows': 100, 
				'clickIndex': 2, 
				'procurement_method_code_exact': '', 
				'rregioncode': '', 
				'project_ctry_name_exact': '', 
				'sectorcode_exact': '', 
				'showrecent': '', 
				'paramValue': '', 
				'activeEndIndex': '10', 
				'sortOrder': '', 
				'deadline_strdate': '', 
				'project_ctry_code_exact': 'IN', 
				'paramKey': 'srt', 
				'procurement_type_exact': '', 
				'submission_enddate': '', 
				'regionname_exact': '', 
				'queryString': 'qterm=&project_ctry_code_exact=IN&srt=submission_date desc,id asc', 
				'deadline_enddate': '', 
				'lang': 'en', 
				'searchString': '', 
				'startIndex': 0, 
				'sector_exact': ''
			}	
	data = urllib.urlencode(params)
	retry = 5
	while retry > 0:
		req = urllib2.Request(url, data)
		try:
			response = urllib2.urlopen(req)
		except HTTPError, e:
			print e.f.read()
			retry = retry - 1
			continue

		resphtml = response.read()
		soup = BeautifulSoup(resphtml)
		for a in soup.findAll('a', href = True):
			if a['href'].startswith('/projects/procurement'): 
				proc_info = get_proc_info('http://www.worldbank.org'+a['href'])
				if not proc_info:
					continue
				push_proc_info(json.dumps(proc_info, default=json_util.default))
	

def push_proc_info(proc_info):
	db_url = 'http://127.0.0.1:8000/procurements'
	retry = 5
	while retry > 0:
		req = urllib2.Request(db_url, proc_info, {'Content-Type':'application/json'})
		try:
			response = urllib2.urlopen(req)
			retry = 0
		except HTTPError, e:
			print e.f.read()
		retry = retry - 1
	print response.read()

def get_proc_info(url):
	retry = 5
	while retry > 0:
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
		except HTTPError, e:
			e.f.read()
			retry = retry - 1
			continue
		resphtml = response.read()
		soup = BeautifulSoup(resphtml)
		proc_info = {}
		try:	
			proc_info['city'] = soup.findAll('td', text='City')[0].findNext().text
			retry = 0
		except IndexError, e:
			print e
			retry = retry - 1
			continue
		proc_info['proc_id'] = str(urlparse.parse_qs(url.split('?')[1])['id'][0])
		proc_info['projectid'] = str(soup.findAll('td', text='Project ID')[0].findNext().text)
		proc_info['proc_url'] = url
		proc_info['title'] = str(soup.findAll('h2', id='primaryTitle')[0].text)
	
	return proc_info

	
if __name__ == '__main__':
	#main()
	pull_procurements()

