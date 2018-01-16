import os
import time
from django.core.files import File
from embryo_website.settings import *

def insertRow(name, phone, bits_id, bits_email):
	# Prepare the dictionary to write
	dict = {}
	dict['name'] = name
	dict['phone'] = phone
	dict['id'] = bits_id
	dict['email'] = bits_email
	dict['time'] = time.strftime('%H:%M:%S')
	with open(os.path.join(MEDIA_ROOT, 'art_registration_details.txt'), "a") as userfile2:
		userfile2.write(bits_id + ",\t" + name + ",\t" + phone + ",\t" + bits_email + ",\t" + time.strftime('%H:%M:%S') + "\n")

	userfile2.close()


