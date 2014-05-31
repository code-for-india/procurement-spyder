import os
from flask import render_template
import mailgun
hosted_at=os.getenv('HOSTED_AT', 'http://127.0.0.1:8000')
def send_verification_mail(email, s_id):
	global hosted_at
	body = render_template('verification-template.html',
			url='%s/verify/%s' % (hosted_at, s_id),
			subscription_id=s_id,
			hosted_at=hosted_at)
	sendmail([email], [], 'Verify your Procurement Spyder subscription', body)

def send_update_mail(email, sectors, locations, s_id):
	global hosted_at
	body = render_template('update-template.html',
			sectors=sectors,
			locations=locations,
			subscription_id=s_id,
			hosted_at=hosted_at)
	sendmail([email], [], 'Your subscription has been updated', body)

def send_welcome_mail(email, sectors, locations, s_id):
	global hosted_at
	body = render_template('welcome-template.html',
			sectors=sectors,
			locations=locations,
			subscription_id=s_id,
			hosted_at=hosted_at)
	sendmail([email], [], 'Your subscription has been confirmed', body)

def send_subscription_mail(email_list, procurement):
	global hosted_at
	body = render_template('subscription-template.html',
			name=procurement['title'],
			url=procurement['proc_url'],
			hosted_at=hosted_at)
	sendmail(email_list, [], 'New Procurement: %s' % procurement['title'] , body)

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
