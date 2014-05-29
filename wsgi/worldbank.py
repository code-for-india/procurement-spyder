import os
import tempfile
import urllib
import urllib2
import urlparse
import json
from bson import json_util
from BeautifulSoup import BeautifulSoup
import database

COUNT=10

def main():
	pull_projects()
	pull_procurements()

def pull_projects():
	wb_url = 'http://search.worldbank.org/api/v2/projects'
	params = {
				'format':'json',
				'source':'IBRD',
				'countryname_exact':'Republic of India',
				'rows':COUNT,
				'kw':'N'
				}
	data = urllib.urlencode(params)
	req = urllib2.Request(wb_url, data)
	response = urllib2.urlopen(req)
	projects_str = response.read()
	projects = json.loads(projects_str)
	for project in projects.get('projects').values():
		database.save_project(project)
	return

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
			retry = 0
		except urllib2.HTTPError, e:
			retry = retry - 1
			continue

		resphtml = response.read()
		soup = BeautifulSoup(resphtml)
		for a in soup.findAll('a', href = True):
			if a['href'].startswith('/projects/procurement'):
				proc_info = get_proc_info('http://www.worldbank.org'+a['href'])
				if not proc_info:
					continue

				database.save_procurement(proc_info)

def get_proc_info(url):
	retry = 5
	proc_info = {}
	while retry > 0:
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
			retry = 0
		except urllib2.HTTPError, e:
			retry = retry - 1
			continue
		resphtml = response.read()
		soup = BeautifulSoup(resphtml)
		try:
			proc_info['city'] = soup.findAll('td', text='City')[0].findNext().text
			retry = 0
		except IndexError, e:
			retry = retry - 1
			continue
		proc_info['proc_id'] = str(urlparse.parse_qs(url.split('?')[1])['id'][0])
		proc_info['projectid'] = str(soup.findAll('td', text='Project ID')[0].findNext().text)
		proc_info['proc_url'] = url
		proc_info['title'] = str(soup.findAll('h2', id='primaryTitle')[0].text)

	return proc_info

if __name__ == '__main__':
	main()

