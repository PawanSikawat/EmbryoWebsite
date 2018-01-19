from django.shortcuts import render
from django.template import RequestContext
from django.core.mail import send_mail,EmailMessage
from database.models import Lecture,Event,Discipline, PagesContent, Gallery, AIC_Discipline,Document
from database.views import *
from embryo_website.forms import SearchForm,RegisterForm,EventForm,AIC_UploadForm,DocumentForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
# from embryo_website.spreadsheet import save_to_spreadsheet
from embryo_website.save_to_file import insertRow
from embryo_website.urlgenerator import *
import os
import datetime
import urllib
# import gdshortener
import base64
def standard():
	dictionary = {}
	image_filenames = []
	dictionary['upcoming_events'] = Event.objects.filter(allowed = True)
	dictionary['upcoming_lectures'] = Lecture.objects.filter(date__gte = datetime.datetime.now(), allowed=True)
	dictionary['recent_lectures'] = recent_lectures()
	return dictionary

def event(request,event_id):
	event_id = int(event_id)
	dictionary = standard()
	dictionary['event'] = Event.objects.get(id = event_id)
	return render(request,'event.htm',dictionary)

def lecturedetail(request,lect_id):
	lect_id = int(lect_id)
	dictionary = standard()
	dictionary['current_lecture'] = get_lecture(lect_id)
	dictionary['presenter_set'] = get_presenter(lect_id)
	return render(request,'lecture_specific.htm',dictionary)
	
def lectures(request,i = 0):
	dictionary = standard()
	i = int(i)
	dictionary['i'] = i
	dictionary['all_lectures'] = get_all_lectures()[i*5:i*5+10]
	dictionary['search_bar'] = SearchForm()
	dictionary['all_discipline'] = Discipline.objects.all()
	if len(dictionary['all_lectures']) > 0:
		dictionary['next']=0
		check_next=get_all_lectures()[(i+1)*5:(i+1)*5+10]
		if len(check_next) > 0:
			dictionary['next']=1;
		return render(request,'lectures.htm',dictionary)
	else:
		i=0
		return HttpResponseRedirect('../')
		

def discipline(request):
	dictionary = standard()
	search_item = request.GET['id']
	if not int(search_item):
		return HttpResponseRedirect('../lectures')
	dictionary['all_lectures'] = get_all_lectures_perd(int(search_item))
	dictionary['search_bar'] = SearchForm()
	dictionary['all_discipline'] = Discipline.objects.all()
	dictionary['current_did'] = Discipline.objects.get(id= (int(search_item)))
	#dictionary['drop_down_menu'] = DisciplineSearch()
	return render(request,'lectures.htm',dictionary)

def rohan(request):
		return HttpResponseRedirect('https://docs.google.com/spreadsheet/viewform?fromEmail=true&formkey=dFFHaUJlanRkRklUbm9uVFBIWWxScnc6MA')

def searching(request):
	dictionary = standard()
	dictionary['search_bar'] = SearchForm()
	search_item = request.GET['search_query']
	if not search_item :
		return HttpResponseRedirect('../lectures')
	dictionary['all_lectures'] = get_all_lectures(search_item)
	return render(request,'lectures.htm',dictionary)

def gallery(request):
	dictionary = standard()
#	all_filenames = os.listdir('/home/hasil/public_html/embryo_website/media/images_gallery')
	all_images_objects = Gallery.objects.filter(allowed = True)
#	image_filenames = []
#	for filename in all_filenames:
#		if filename.endswith('png') or filename.endswith('jpg') or filename.endswith('PNG') or filename.endswith('JPG'):
#			image_filenames.append(filename)
#	dictionary['all_images'] = image_filenames
#	all_filenames = [str(x.photo.name.split('/')[-1]) for x in all_images_objects]
	dictionary['all_images'] = all_images_objects
	return render(request,'gallery.htm',dictionary)

def newsletters(request):
	dictionary = standard()
	dictionary['newsletters'] = get_all_newsletter().filter(allowed=True)
	return render(request,'newsletter.htm',dictionary)
	
def writeup(request, name = 'home'):
	dictionary = standard()
	dictionary['writeup']=PagesContent.objects.get(link=name)
	return render(request,'content.htm',dictionary)
	
	
def eventregister(request):
	dictionary = standard()
	dictionary['sent'] = True
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form = form.cleaned_data
			name = form['name']
			bits_id = form['bits_id']
			year = bits_id[0:4]
			if bits_id[4] in ['A','B','C','D']:
				degree = 'f'
			else:
				degree = 'h'
			
			email_id = bits_id[len(bits_id)-4:len(bits_id)-1]
			mailid = year + email_id
			bits_email = degree + year + email_id + "@pilani.bits-pilani.ac.in"
			phone = form['phone_number']
			if not (bits_id.endswith('P') or bits_id.endswith('p')):
				dictionary['form'] = EventForm(request.POST)
				dictionary['wid'] = True
				return render(request,'eventreg.htm',dictionary,)
			if not (len(phone) >= 10 and  phone.isdigit()):
				dictionary['form'] = EventForm(request.POST)
				dictionary['nophone'] = True
				return render(request,'eventreg.htm',dictionary,)
			if not mailid.isdigit():
				dictionary['form'] = EventForm(request.POST)
				dictionary['noemail'] = True
				return render(request,'eventreg.htm',dictionary,)
			subject = "ART 2015 Registration"
			body = make_url(request.get_host(),name,bits_id,phone,bits_email)
			success = send_mail(subject,body,"embryoclub@gmail.com",[bits_email,],fail_silently = False)
			dictionary['mail'] = bits_email
			dictionary['name'] = name
			dictionary['success'] = success
			#insertRow(name, phone, bits_id, bits_email)
			return render(request,'eventreg.htm',dictionary,)
		else:
			dictionary['form'] = EventForm(request.POST)
	else:
		dictionary['form'] = EventForm()
	return render(request,'eventreg.htm',dictionary,)

def get_from_mail(request):
	if(request.GET.get('params')):
		paramters = request.GET.get('params')
		return HttpResponseRedirect('http://' + request.get_host() +'/testsuccess/'+ base64.b64decode(paramters))
	else:
		dictionary = standard()
		name = request.GET.get('name')
		phone_number = request.GET.get('phone_number')
		bits_id = request.GET.get('bits_id').swapcase()
		bits_email = request.GET.get('bits_email')
		insertRow(name, phone_number, bits_id, bits_email)
		dictionary['name'] = name
		return render(request,'regsuccess.htm', dictionary,)

def art_success(request):
	dictionary = standard()
	return render(request,'ethankyou.htm', dictionary,)

	
def redirect(request):
	return HttpResponseRedirect('../nothankyou')

def register(request):
	dictionary = standard()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../thankyou')
		dictionary['form'] = form
	else:
		dictionary['form'] = RegisterForm()
	return render(request,'register.htm',dictionary,)
	
def notfound(request):
	dictionary = standard()
	return render(request,'404.htm',dictionary)

def redirector(request):
	a=str(request.get_full_path())
	b=a.split('.')[0]
	if b == '/index' :
		return HttpResponseRedirect('../')
	elif b == '/faqs':
		return HttpResponseRedirect('../faq')
	else: 
		return HttpResponseRedirect(b)

def atmosdetail(request,atmos_id):
	atmos_id = int(atmos_id)
	dictionary = standard()
	dictionary['current_atmos'] = get_atmos(atmos_id)
				
	return render(request,'atmos_specific.htm',dictionary)

def atmos_list(request,page_id=0):
	page_id = int(page_id)
	dictionary = standard()
	dictionary['page_id'] = page_id
	dictionary['all_atmos_lectures'] = get_all_atmos_lectures()[page_id:page_id+5]
	dictionary['all_discipline'] = Discipline.objects.all()
											
	return render(request,'atmos_list.htm',dictionary)


def aic(request):
	dictionary = standard()
	dictionary['aic_disciplines'] = AIC_Discipline.objects.all()
	return render(request,'aic.htm', dictionary,)

def aic_track(request, discipline_id):
	discipline_id = int(discipline_id)
	dictionary = standard()
	dictionary['companies'] = get_companies(discipline_id)
	dictionary['discipline'] = get_discipline(discipline_id)
	dictionary['aic_disciplines'] = AIC_Discipline.objects.all()
	return render(request,'aic_companies.htm', dictionary,)

def company_details(request, company_id):
	company_id = int(company_id)
	dictionary = standard()
	dictionary['company'] = get_specific_company(company_id)
	dictionary['submission_date'] = dictionary['company'].submission_date.date()
	if(dictionary['company'].submission_date.date()>=datetime.datetime.now().date()):
		dictionary['is_active'] = 1==1
	else:
		dictionary['is_active'] = 1==0
	dictionary['aic_disciplines'] = AIC_Discipline.objects.all()
	return render(request,'company_details.htm', dictionary,)

def company_register(request, company_id):
	company_id = int(company_id)
	dictionary = standard()
	dictionary['company'] = get_specific_company(company_id)
	if request.method == 'POST':
		form = AIC_UploadForm(request.POST)
		if form.is_valid():
			cleaned_form = form.cleaned_data
			form.save()
			subject = "[BITS Embryo] Apogee Innovation Challenge Registration"
			host= request.get_host()
			member_one_email = cleaned_form['member_one_email']
			body = "Hi Team " + str(cleaned_form['team_name']) + "!\n\nYou have successfully registered for the company " + str(dictionary['company']) + ". The following are your details: \n\n" + "Team Name: " + str(cleaned_form['team_name']) + "\nProject Name: " + str(cleaned_form['project_name']) + "\n\nSolution Upload Link: " +  str(make_upload_url(host,cleaned_form['team_name'],cleaned_form['member_one_name'],company_id)) + "\n\nPlease click on the above link to upload your solution. (Only One Member is required to submit the solution.)\n\nRegards,\nBITS Embryo.\nEmail: embryoclub@gmail.com\nContact: Rohan, +91-9660582805."
			success = send_mail(subject,body,"embryoclub@gmail.com",[cleaned_form['member_one_email'],cleaned_form['member_two_email'],cleaned_form['member_three_email'],cleaned_form['member_four_email'],cleaned_form['member_five_email']],fail_silently = False)
			return render(request,'company_register_success.htm', dictionary,)
	dictionary['register_form'] = AIC_UploadForm()
	dictionary['submission_date'] = dictionary['company'].submission_date.date()
	if(dictionary['company'].submission_date.date()>=datetime.datetime.now().date()):
		dictionary['is_active'] = 1==1
	else:
		dictionary['is_active'] = 1==0
	dictionary['aic_disciplines'] = AIC_Discipline.objects.all()
	return render(request,'company_register.htm', dictionary,)

def company_upload(request, company_id):
	company_id = int(company_id)
	if(request.GET.get('params')):
		paramters = request.GET.get('params')
		print( base64.b64decode(paramters))
		return HttpResponseRedirect('http://' + request.get_host() +'/company_thank_you/' + str(company_id) + '/' + base64.b64decode(paramters))
	
def company_thank_you(request, company_id):
	company_id = int(company_id)
	company = get_specific_company(company_id)
	dictionary = standard()
	dictionary['company'] = company
	if(request.GET.get('name')):
		team_name_render = request.GET.get('name')
		dictionary['team_name_render'] = team_name_render
	
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.team_name = request.POST['team_name']
			newdoc.company_name = company.company_name
			newdoc.save()
			#sending an email
			subject = "[BITS Embryo] Apogee Innovation Challenge Successful Submission"
			body = "Hi Team " + str(request.POST['team_name']) + "!\n\nYou have successfully submitted the solution for the company " + str(dictionary['company']) + ". The following are your details: \n\n" + "Team Name: " + str(request.POST['team_name']) + ". The solution submitted is attached.\n\nRegards,\nBITS Embryo.\nEmail: embryoclub@gmail.com\nContact: Rohan, +91-9660582805."          
			print( request.POST['team_name'])
			to = get_mail_ids(request.POST['team_name'])  
			email = EmailMessage(subject,body,'embryoclub@gmail.com',to)
			basepath = os.path.dirname(os.path.abspath(__file__))
			print( str(basepath))
			filepath = os.path.join(basepath, './../media/Company_Solutions/', company.company_name, str(request.POST['team_name']).upper(), str(request.FILES['docfile']))
			print( str(filepath))
			email.attach_file(filepath)
			email.send(fail_silently=False)
			# Redirect to the document list after POST
			
			return render(request,'company_thank_you.htm', dictionary,)
	else:
		dictionary_temp = dict()
		dictionary_temp['team_name'] = team_name_render
		form = DocumentForm(dictionary_temp, auto_id=False) # A empty, unbound form
		print( team_name_render)
		print( str(form))
	dictionary['form'] = form
	
	dictionary['company_id'] = company_id
	return render(request,'company_upload.htm', dictionary,)


