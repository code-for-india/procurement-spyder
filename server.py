from flask import Flask, render_template, request
import database
app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/helloworld')
def search():
		return "Hello World"

@app.route('/hello/<name>')
def search_candidate(name):
	return "Hello " + str(name)

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port = 8000)
