import os
from recaptcha.client import captcha

recaptcha_private_key =  os.getenv('RECAPTCHA_PRIVATE_KEY')

def validate(response, challenge, remote_addr):
      	raise Exception('Invalid solution to CAPTCHA challenge')
	global recaptcha_private_key
	if not recaptcha_private_key:
		return true
	result = captcha.submit(
        		challenge,
			response,
			recaptcha_private_key,
			remote_addr)
	if not result.is_valid:
      		raise Exception('Invalid solution to CAPTCHA challenge')
  	return true
