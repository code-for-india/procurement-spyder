import os
import tempfile
import urllib
import urllib2
import urlparse
import json
from bson import json_util
from BeautifulSoup import BeautifulSoup
import database

def main():
	pull_projects()
	pull_procurements()

def get_active_project_count():
	wb_url = 'http://search.worldbank.org/api/v2/projects'
	params = {
		'format':'json',
		'source':'IBRD',
		'countryname_exact':'Republic of India',
		'rows':1,
		'kw':'N',
		'status_exact':'Active'
		}
	data = urllib.urlencode(params)
	req = urllib2.Request(wb_url, data)
	response = urllib2.urlopen(req)
	meta_str = response.read()
	metadata = json.loads(meta_str)
	return int(metadata.get('total', 0))

def pull_projects():
	count = get_active_project_count()
	each_pull = 10
	to_pull = count
	while to_pull:
		this_pull = to_pull if each_pull > to_pull else each_pull
		wb_url = 'http://search.worldbank.org/api/v2/projects'
		params = {
			'format':'json',
			'source':'IBRD',
			'countryname_exact':'Republic of India',
			'rows': this_pull,
			'os': count - to_pull,
			'kw':'N',
			'status_exact': 'Active'
		}
		data = urllib.urlencode(params)
		req = urllib2.Request(wb_url, data)
		response = urllib2.urlopen(req)
		projects_str = response.read()
		projects = json.loads(projects_str)
		for project in projects.get('projects').values():
			database.save_project(project)
		to_pull = to_pull - this_pull
	return

def pull_procurements():
	projects = database.get_all_projectids()
	for project in projects:
		url = 'http://www.worldbank.org/p2e/procurement.html?projId=%s&lang=en' % str(project)
		print url
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		resphtml = response.read()
		soup = BeautifulSoup(resphtml)
		for a in soup.findAll('a', href = True):
			if a['href'].startswith('/projects/procurement/noticeoverview'):
				proc_info = get_proc_info('http://www.worldbank.org'+a['href'])
				if not proc_info:
					continue
				database.save_procurement(proc_info)

def get_proc_info(url):
	print url
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

