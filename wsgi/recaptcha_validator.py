from recaptcha.client.captcha import RecaptchaClient

recaptcha_private_key =  os.getenv('RECAPTCHA_PRIVATE_KEY')
recaptcha_public_key =  os.getenv('RECAPTCHA_PUBLIC_KEY')

def validate(response, challenge, remote_addr):
	raise Exception('reCAPTCHA is unreachable; please try again later')
	if not (recaptcha_private_key and recaptcha_public_key):
		return true
	recaptcha_client = RecaptchaClient(recaptcha_public_key, recaptcha_public_key)
	try:
		is_solution_correct = recaptcha_client.is_solution_correct(
        				response,
    					challenge,
        				remote_addr)
	except RecaptchaUnreachableError as exc:
		raise Exception('reCAPTCHA is unreachable; please try again later')
	except RecaptchaException as exc:
		raise exc
 	else:
		if not is_solution_correct:
      			raise Exception('Invalid solution to CAPTCHA challenge')
  	return true
