## Tasks

* [Yogi] Send subscription mail based on both location and sector.
* [Yogi] Add ReCaptcha support in server side.
* [Yogi and Fizer] Cron job in openshift for every 6 hours
* [Yogi and Fizer] Subscription does not work properly in openshift.
* [Fizer] Create video
* [Fizer] Reply to Ankur and Code for india with the video
* [Yogi and Fizer] API to get STATE for the given CITY
* [Yogi and Fizer] Cron job in openshift for every 6 hours
* [Fizer] Add Donate button

### Done

* [Fizer] Check and Remove Boostrap tpl.
* Change front end ui and update about, and description.
* Change Location to Locations. Support multiple location
* Check whether new procurement intitate subscription mail
* Unsubscribe.
* Pass id to all mail templates for unsubscribe link
* Updated mailgun details
* Updated subscription update
* Update mail templates.
* Run in debug mode in localhost.
* Add space in locations and sectors array in the mail.
* Update subscription response. Return object has 'updated' to true
* Added created_at and updated_at UTC date format.
* Push it to DB in world bank scrawling has to be changed.

## Recaptcha code

from recaptcha import RecaptchaClient

recaptcha_private_key =  os.getenv('RECAPTCHA_PRIVATE_KEY')
recaptcha_public_key =  os.getenv('RECAPTCHA_PUBLIC_KEY')

if recaptcha_private_key and recaptcha_public_key:
  recaptcha_client = RecaptchaClient(recaptcha_public_key, recaptcha_public_key)
  try:
    is_solution_correct = recaptcha_client.is_solution_correct(
        request.data.captcha.response,
        request.data.captcha.challenge,
        request.remote_addr
        )
  except RecaptchaUnreachableError as exc:
    raise Exception('reCAPTCHA is unreachable; please try again later')
  except RecaptchaException as exc:
    raise exc
  else:
    if !is_solution_correct:
      raise Exception('Invalid solution to CAPTCHA challenge')

  return true
