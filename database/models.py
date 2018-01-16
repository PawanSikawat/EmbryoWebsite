from django.db import models
from tinymce.models import HTMLField
from django.core.files.storage import FileSystemStorage
import os

def get_upload_path(instance, filename):
    return os.path.join('./Company_Solutions/', instance.company_name, instance.team_name.upper(), filename)

class Discipline(models.Model):
	stream = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.stream
		
class Presenter(models.Model):
    name = models.CharField(max_length = 50,db_column='Name')
    credentials = HTMLField(help_text ='Enter the current designation of the speaker, and past work experience',db_column='Credentials', blank=True)
    profile = HTMLField(help_text = 'Enter the qualification and other details',db_column='Profile')
    email = models.EmailField('e-mail',max_length=50, blank = True)
    address = HTMLField(blank = True)
    class Meta:
        db_table = u'presenters'
    def __unicode__(self):
    #name in actual database contain NoneType in name and can't remove them because this will change the present id but which is used as foreign key
     a = str(self.name)
     return unicode(a)


class Lecture(models.Model):
    date = models.DateTimeField(null=True)
    discipline = models.ManyToManyField(Discipline)
    topic = models.CharField(max_length= 500)
    moreinfo = HTMLField(blank=True)
    presenter = models.ForeignKey(Presenter, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to = ('Speakerphotos'),max_length=50, blank=True)
    discussion = models.TextField(blank=True)
#    feedback = models.FileField(upload_to = ("./feedback"), blank = True)
    allowed = models.BooleanField('Display on site',default = True)
    venue = models.CharField(max_length = 100)
    campus = models.CharField(max_length=50)
    class Meta:
        db_table = u'lectures'
    def __unicode__(self):
       return self.topic
    
       
class Feedback(models.Model):
	lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
	feedback = models.FileField(upload_to = ("feedback"), blank = True)
	slides = models.FileField(upload_to = ('slides'), max_length = 150, blank = True)
	video_link = models.URLField(max_length = 50, blank = True)
	poster = models.ImageField(upload_to = ('posters'),max_length = 150 ,blank = True)

class Newsletter(models.Model):
	name = models.CharField(max_length = 150)
	newsletter = models.FileField(upload_to = ('newsletters'), max_length = 150)
	allowed = models.BooleanField('Publish on site',default = True)
	def __unicode__(self):
		a= self.newsletter.name
		a = a.split('/')
		return a[-1]

class LecturesDiscipline(models.Model):
	lecture_id = models.CharField(max_length = 50)
	discipline_id = models.CharField(max_length = 50)
	class Meta:
		db_table = u'lec_discipline' 
	def __unicode__(self):
		return unicode(self.lecture_id)

class Event(models.Model):
	image = models.ImageField(upload_to = ('events'))
	allowed = models.BooleanField(default = True)
	description = HTMLField()
	name = models.CharField(max_length = 50)
	def __unicode__(self):
		a = self.image.name
		a = a.split('/')
		return a[-1]

class SignUp(models.Model):
	first_name = models.CharField('First Name*', max_length = 50)
	last_name = models.CharField('Last Name*', max_length = 50)
	email = models.EmailField('E-mail*',max_length = 50)
	alumni = models.BooleanField('Are you an alumni?')
	batch = models.IntegerField()
	address = models.TextField(blank = True)
	discipline_first = models.CharField(max_length = 50,blank = True,  default='Other')
	discipline_dual = models.CharField(max_length = 50,blank = True,  default='Not Applicable')
	phone = models.CharField(max_length = 13,blank = True, default='+91')
	biography = models.TextField('Short Biography',blank = True)
	lect_topics = models.TextField('What topics would you like to give the lecture on?*')
	talk_discipline = models.CharField('Select the Discipline that matches the topics you wish to deliver a talk on', max_length = 50,blank = True,  default='Interdisciplinary')
	def __unicode__(self):
		return "%s %s" % (self.first_name,self.last_name)

class PagesContent(models.Model):
	name = models.CharField('Page Name', max_length=50)
	link = models.CharField('Page Link', max_length=50, blank = True)
	content=HTMLField('Put content of page here')
	def __unicode__(self):
		return self.link
	class Meta:
		verbose_name_plural = "Pages Content"

class Gallery(models.Model):
	name = models.CharField('Heading', max_length = 50,blank = True)
	photo = models.ImageField(upload_to = ('images_gallery'),max_length=50)
	details = models.TextField(blank = True)
	allowed = models.BooleanField(default = True)
	def __unicode__(self):
		a = self.photo.name
		a = a.split('/')
		return a[-1]
	class Meta:
		verbose_name_plural = "Gallery"

class Atmos(models.Model):
	date = models.DateTimeField(null=True)
	discipline = models.ManyToManyField(Discipline)
	topic = HTMLField(max_length= 50, null = True)
	moreinfo = HTMLField(blank=True)
	#presenter = models.ForeignKey(Presenter, on_delete=models.PROTECT)
	photo = models.ImageField(upload_to = ("AtmosPhotos"),max_length=50, blank=True)
	discussion = models.TextField(blank=True)
	#feedback = models.FileField(upload_to = ("./feedback"), blank = True)
	allowed = models.BooleanField('Display on site',default = True)
	venue = models.CharField(max_length = 10)
	campus = models.CharField(max_length=10)
	class Meta:
		db_table = u'atmos'
	def __unicode__(self):
		return self.topic


class AIC_Discipline(models.Model):
	stream = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.stream

class AIC_Company(models.Model):
	submission_date = models.DateTimeField(null=True)
	discipline = models.ManyToManyField(AIC_Discipline)
	company_name = models.CharField(max_length = 100)
	company_description = HTMLField(blank=True)
	logo = models.ImageField(upload_to = ("./AIC_CompanyPhotos"),max_length=50, blank=True)
	problem_statement_details = models.TextField(blank=True)
	problem_statement_file = models.FileField(upload_to = ("./Problem_Statements"), blank = True)
	allowed = models.BooleanField('Display on site',default = True)
	class Meta:
		db_table = u'aic_company_details'
	def __unicode__(self):
		return self.company_name

class AIC_Solution(models.Model):
	team_name = models.CharField('Team Name* (Create any single word teamname.)   ',max_length = 100,blank=False)
	project_name = models.CharField('Project Name* (Preferably Problem Name.)   ',max_length = 100, blank=False)
	member_one_name = models.CharField('Member One Name*   ',max_length = 100,blank=False)
	member_one_email = models.EmailField('Member One Email*   ',blank=True)
	member_two_name = models.CharField('Member Two Name   ', max_length = 100,blank=True)
	member_two_email = models.EmailField('Member Two Email   ', blank=True)
	member_three_name = models.CharField('Member Three Name   ', max_length = 100,blank=True)
	member_three_email = models.EmailField('Member Three Email   ', blank=True)
	member_four_name = models.CharField('Member Four Name   ', max_length = 100,blank=True)
	member_four_email = models.EmailField('Member Four Email   ', blank=True)
	member_five_name = models.CharField('Member Five Name   ', max_length = 100,blank=True)
	member_five_email = models.EmailField('Member Five Email   ', blank=True)
	description = models.TextField('Briefly describe your solution (at max 500 characters.)    ',blank=True)
	company_discipline = models.CharField('Choose the track under which you are applying for the company*', max_length=50,blank=False,default='Not Applicable')
	def __unicode__(self):
		return self.team_name

class Document(models.Model):
	team_name = models.CharField(max_length=100)
	company_name = models.CharField(max_length=100)
	docfile = models.FileField(upload_to=get_upload_path)
