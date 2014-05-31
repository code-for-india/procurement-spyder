import os
from flask import Flask, request, url_for, redirect
import database
import json
from bson import json_util
import mailer
import recaptcha_validator

app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
@app.route('/about')
@app.route('/subscribe')
@app.route('/verify')
@app.route('/verify-failed')
@app.route('/success')
@app.route('/updated')
@app.route('/unsubscribed')
def index():
	return app.send_static_file('index.html')

@app.route('/projects', methods=["GET"])
def projects():
	'''
	Function to get projects
	'''
	if request.method == 'GET':
		return database.get_all_projects()

@app.route('/procurements', methods=["GET"])
def procurements():
	'''
	Function to get procurements
	'''
	if request.method == 'POST':
		proc_resp = database.create_procurement(request.data)
		if not proc_resp:
			return '', 409
		proc_dict = json.loads(proc_resp)
		subscribers = database.get_subscribers(proc_dict)
		print 'SUBSCRIBERS-------------', subscribers
		if subscribers:
			mailer.send_subscription_mail(subscribers, proc_dict)
		return proc_resp, 201
	elif request.method == 'GET':
		return database.get_all_procurements()

@app.route('/subscriptions', methods=["POST"])
def subscriptions():
	'''
	Function to create subscriptions
	'''
	dict_subscription = json.loads(request.data)
	# try:
	# 	recaptcha_validator.validate(
	# 		dict_subscription['captcha']['response'],
  #       		dict_subscription['captcha']['challenge'],
  #       		request.remote_addr)
	# except Exception as e:
	# 	err = {}
	# 	err['message'] = str(e)
	# 	return json.dumps(err, default=json_util.default), 400

	subscription_resp, created, s_id = database.create_subscription(dict_subscription)
	subscription = json.loads(subscription_resp)
	print subscription
	if created:
		mailer.send_verification_mail(subscription['email'], s_id)
		return redirect('/verify')
	else:
		mailer.send_update_mail(subscription['email'],
			', '.join(subscription['sectors']),
			', '.join(subscription['locations']),
			s_id)
	return subscription_resp, 201

# Unsubscribe
@app.route('/unsubscribe/<_id>', methods=["GET"])
def unsubscribe(_id):
	'''
	Function to unsubscribe
	'''
	database.delete_subscription(_id)
	return redirect('/unsubscribed')

# Verify email address
@app.route('/verify/<token>', methods=["GET"])
def verify_token(token):
	'''
	Function to verify subscription by token
	'''
	subscription = database.verify_subscription(token)
	if subscription:
		mailer.send_welcome_mail(subscription['email'],
			', '.join(subscription['sectors']),
			', '.join(subscription['locations']),
			str(subscription['_id']))
		return redirect('/success')
	return redirect('/verify-failed')


if __name__ == '__main__':
	app_name = os.getenv('OPENSHIFT_APP_NAME')
	# run in debug mode in development
	if app_name is None:
		app.run(debug = True, host = '0.0.0.0', port = 8000)
	else:
		app.run()
