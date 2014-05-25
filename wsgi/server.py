import os
from flask import Flask, render_template, request
import database
import mailgun
import json
app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
@app.route('/success')
@app.route('/updated')
@app.route('/unsubscribed')
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
		proc_resp = database.create_procurement(request.data)
		if not proc_resp:
			return '', 409
		proc_dict = json.loads(proc_resp)
		subscribers = database.get_subscribers(proc_dict)
		print 'SUBSCRIBERS-------------', subscribers
		if subscribers:
			send_subscription_mail(subscribers, proc_dict)
		return proc_resp, 201
	elif request.method == 'GET':
		return database.get_all_procurements()

@app.route('/subscriptions', methods=["POST"])
def subscriptions():
	'''
	Function to create subscriptions
	'''
	subscription_resp, created = database.create_subscription(request.data)
	subscription = json.loads(subscription_resp)
	print subscription
	if created:
		send_welcome_mail(subscription['email'], ','.join(subscription['sectors']))
	else:
		send_update_mail(subscription['email'], ','.join(subscription['sectors']))
	return subscription_resp, 201


#GET /sendmail
@app.route('/sendmail', methods=["GET"])
def sendmail(to_list, bcc_list, subject, body):
	mail = {
			"from": "Procurement Spyder <no-reply@chennainerd.in>",
			"to": to_list,
	    	"bcc": bcc_list,
	    	"subject": subject,
	    	"html": body
			}
	mailgun.send_simple_message(mail)
	return ''

def send_update_mail(email, sectors):
	body = render_template('update-template.html', sectors=sectors)
	sendmail([email], [], 'Your subscription has been updated', body)

def send_welcome_mail(email, sectors):
	body = render_template('welcome-template.html', sectors=sectors)
	sendmail([email], [], 'Your subscription has been confirmed', body)

def send_subscription_mail(email_list, procurement):
	body = render_template('subscription-template.html', name=procurement['title'], url=procurement['proc_url'])
	sendmail(email_list, [], 'New Procurement: %s' % procurement['title'] , body)

if __name__ == '__main__':
	app_name = os.getenv('OPENSHIFT_APP_NAME')
	# run in debug mode in development
	if app_name is None:
		app.run(debug = True, host = '0.0.0.0', port = 8000)
	else:
		app.run()
