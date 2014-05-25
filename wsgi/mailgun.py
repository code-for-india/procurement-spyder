import requests
import os
def send_simple_message(mydata):
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    return requests.post(
        "https://api.mailgun.net/v2/chennainerd.in/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": mydata.get('from'),
              "to": mydata.get('to'),
              "cc": mydata.get('cc'),
              "bcc": mydata.get('bcc'),
              "subject": mydata.get('subject'),
              #"text": mydata.get('text', ''),
              "html": mydata.get('html', '') })

def get_data():
	return {
				"from": "Procurement Spyder <no-reply@chennainerd.in>",
				"to": "Dheeraj <fizerkhan@gmail.com>",
				#"cc": ["Dj <dheerajjoshi@outlook.com>","Joshi <dheerajjoshi1991@yahoo.co.in>"],
				#"bcc": ["Dj <dheerajjoshi@outlook.com>"],
				"subject": "Hello World",
				#"text": "Testing Text :::: 1234567890"
				"html": "<html>Testing HTML <b>Bold</b><i>Italics</i><u>Underline</u></html>"
			}

if __name__ == "__main__":
	mydata = get_data()
	send_simple_message(mydata)
