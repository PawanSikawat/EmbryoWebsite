import time
import gdata.spreadsheet.service
import gspread
email = 'embryoclub@gmail.com'
password = 'mbry0pr0'
def save_to_spreadsheet(name,num,bits_id,bits_email):
	spreadsheet_key = '1YgpIc-HD2ADndEzgCjn-v8w7hGFbbsuM5exoJmPbouA'
	worksheet_id = 'od6'
	spr_client = gdata.spreadsheet.service.SpreadsheetsService()
	spr_client.email = email
	spr_client.password = password
	spr_client.source = 'ART 2015 Registration'
	spr_client.ProgrammaticLogin()
	dictionary = {}
	dictionary['id'] = bits_id.swapcase()
	dictionary['name'] = name
	dictionary['email'] = bits_email
	dictionary['time'] = time.strftime('%H:%M:%S')
	entry = spr_client.InsertRow(dictionary,spreadsheet_key,worksheet_id)
	return 1
		
