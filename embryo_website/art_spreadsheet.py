#!/usr/bin/python
import time
import gdata.spreadsheet.service

email = 'embryoclub@gmail.com'
password = 'mbry0pr0'

# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = '1YgpIc-HD2ADndEzgCjn-v8w7hGFbbsuM5exoJmPbouA'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'

spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Example Spreadsheet Writing Application'
spr_client.ProgrammaticLogin()

def insertRow(name, phone, bits_id, bits_email):
	dict = {}
	dict['name'] = name
	dict['phone'] = phone
	dict['id'] = bits_id
	dict['email'] = bits_email
	dict['time'] = time.strftime('%H:%M:%S')
	entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
	
