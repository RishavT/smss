#!/usr/bin/python
import gdata.service
import gdata.calendar.service
import gdata.docs.service
import gdata.contacts.client
import gdata.contacts.service

application_name = 'RTR-sms-bot'

client = gdata.contacts.client.ContactsClient()
def login(email,password):
	try:
		client.ClientLogin(email, password, application_name)
	except gdata.service.CaptchaRequired:
		answer = raw_input('Answer to the challenge? ')
		client.ClientLogin(email=email, password=password, source=application_name, captcha_token=client.captcha_token,captcha_response=answer)
		return (True,0)
	except gdata.service.BadAuthentication:
		return (False,"Invalid Username/Password")
	except gdata.service.Error:
		return (False,"Could not login. Please try later")
	return (True,1)
def getcontacts():
	a = gdata.contacts.client.ContactsQuery(max_results=10000)
	contacts_feed = client.GetContacts(q=a)

	return_value = [('','')]
	for i,entry in enumerate(contacts_feed.entry):
		name = ''
		phone = ''
		entry_str = ''
		if entry.name:
			name = entry.name.full_name.text
		for ph in entry.phone_number:
			if ph:
				phone = ph.text
		if len(name)>0:
			if len(phone)>0:
				if i == 0:
					return_value[0] = (name,phone)
				else:
					return_value += [(name,phone)]
	return return_value
