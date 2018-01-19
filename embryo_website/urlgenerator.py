import urllib
# import gdshortener
import base64
def make_url(host,name,bits_id,phone_number,bits_email):
	#s = gdshortener.ISGDShortener()
	#a = s.shorten('http://'+host + '/' + 'testsuccess' + '/' + '?name='+urllib.quote_plus(name)+'&bits_id='+urllib.quote_plus(bits_id)+'&phone_number='+urllib.quote_plus(phone_number)+'&bits_email='+urllib.quote_plus(bits_email))
	parameters = base64.b64encode('?name='+urllib.quote_plus(name)+'&bits_id='+urllib.quote_plus(bits_id)+'&phone_number='+urllib.quote_plus(phone_number)+'&bits_email='+urllib.quote_plus(bits_email))
	a = 'http://'+host + '/' + 'testsuccess' + '/' + '?params=' +parameters 
	return a

def make_upload_url(host,team_name,email,company_id):
	parameters = base64.b64encode('?name='+urllib.quote_plus(team_name)+'&email='+urllib.quote_plus(email))
	link = 'http://'+host + '/' + 'company_upload' + '/' + str(company_id) + '/' + '?params=' +parameters
	return link
