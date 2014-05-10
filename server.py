from flask import Flask, render_template, request
import database
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

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port = 8000)
