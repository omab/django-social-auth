twilio-backend
==============


* Register a new application at [Twilio Connect Api](https://www.twilio.com/user/account/connect/apps)

* fill `TWILIO_CONNECT_KEY` and `TWILIO_AUTH_TOKEN` values in the settings:


    `TWILIO_CONNECT_KEY = ''
     TWILIO_AUTH_TOKEN = ''
`

* Add desired authentication backends to Django's `AUTHENTICATION_BACKENDS` setting:

        `'social_auth.backends.contrib.twilio.TwilioBackend',`

* Usage example
	
	`<a href="{% url socialauth_begin 'twilio' %}">Enter using Twilio</a>`