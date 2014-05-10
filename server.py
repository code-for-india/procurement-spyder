from flask import Flask, render_template, request
import database
import mailgun
app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/projects', methods=["POST", "GET"])
def projects():
	'''
	Function to create/get projects
	'''
	if request.method == 'POST':
		print request.data
		return database.create_projects(request.data), 201
	elif request.method == 'GET':
		return database.get_all_projects()

@app.route('/comments', methods=["POST", "GET"])
def comments():
	'''
	Function to add comment and read comments
	'''
	pass

@app.route('/procurements', methods=["POST", "GET"])
def procurements():
	'''
	Function to create procurement/get procurements
	'''
	if request.method == 'POST':
		return database.create_procurement(request.data), 201	
	elif request.method == 'GET':
		return database.get_all_procurements()

@app.route('/subscriptions', methods=["POST"])
def subscriptions():
	'''
	Function to create subscriptions
	'''
	print request.data
	return database.create_subscription(request.data), 201


#GET /sendmail
@app.route('/sendmail', methods=["GET"])
def sendmail():
	mail = {
			"from": "Procurement Spy<postmaster@sandbox381bc65cf9a0430cb057afb272d83c3a.mailgun.org>",
	    "to": 'fizerkhan@gmail.com',
	    "subject": 'You are awesome',
	    "html": render_template('mail-template.html', projectName='Roadsow')
			}
	mailgun.send_simple_message(mail)
	return ''

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port = 8000)
