# EmbryoWebsite
Website for http://www.embryo.bits-pilnai.ac.in
Installation instruction:
* git clone https://github.com/EmbryoWebsite/EmbryoWebsite
* cd EmbryoWebsite
* Install python3 and pip.
* pip install virtualenv
* virtualenv venv -p python3
* source venv/bin/activate
* pip install django==2.0.1
* pip install django-tinymce
* pip install django-admin_tools
* ./manage.py createsuperuser
* ./manage.py runserver
