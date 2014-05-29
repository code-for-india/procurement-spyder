from flask import render_template
import mailgun

def send_update_mail(email, sectors, locations, s_id):
	body = render_template('update-template.html', sectors=sectors, locations=locations, subscription_id=s_id)
	sendmail([email], [], 'Your subscription has been updated', body)

def send_welcome_mail(email, sectors, locations, s_id):
	body = render_template('welcome-template.html', sectors=sectors, locations=locations, subscription_id=s_id)
	sendmail([email], [], 'Your subscription has been confirmed', body)

def send_subscription_mail(email_list, procurement):
	body = render_template('subscription-template.html', name=procurement['title'], url=procurement['proc_url'])
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

