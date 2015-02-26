# include docs/Makefile

.PHONY: base_requirements dev_requirements prod_requirements static clean_template
.SILENT: deps

# virtualenv variables
VIRTUALENV_PATH    := $(shell cd env && pwd)
VIRTUALENV_ACTIVATE := $(VIRTUALENV_PATH)/bin/activate
VIRTUALENV_PYTHON   := $(VIRTUALENV_PATH)/bin/python

getdeb    = [ -z "`dpkg -l | grep $(1)`" ] && sudo apt-get install $(1) || :
#notify    = @[ -f "$(HOME)/hipchat-message" ] && $(HOME)/hipchat-message $(1) || :

DIR := $(shell basename $(CURDIR))

help:
	@echo
	@echo ----------------------------------------------------------------------
	@echo -------------------------- OWL Starter -------------------------------
	@echo ----------------------------------------------------------------------
	@echo
	@echo "   - install     Install the application for Production"
	@echo "   - develop     Install the application for development"
	@echo "   - deps        Install all system dependencies using apt-get"
	@echo "   - static      Collect static files"
	@echo "   - superuser   Create a super user in production"
	@echo "   - server      Serve project for development"
	@echo "   - html        Make documentation"
	@echo "   - live        Watch Documentation changes"
	@echo
	@echo ----------------------------------------------------------------------
	@echo "   - template                       Create a template based on this"
	@echo "   - project NAME=project_name      Create a project based on this"
	@echo "                                    (default_name={{ project_name }}_project)"
	@echo ----------------------------------------------------------------------
	@echo

develop: deps env var dev_requirements cleancache static db_dev
install: env var prod_requirements cleancache static db_prod

superuser: deps env var prod_requirements cleancache static
	DJANGO_SETTINGS_MODULE=settings.production ./env/bin/python app/manage.py createsuperuser


db_prod:
	DJANGO_SETTINGS_MODULE=settings.production ./env/bin/python app/manage.py makemigrations
	DJANGO_SETTINGS_MODULE=settings.production ./env/bin/python app/manage.py migrate
	DJANGO_SETTINGS_MODULE=settings.production ./env/bin/python app/manage.py syncdb
	@echo "Migrations in Production applied..."

db_dev: deps env var requirements cleancache static
	DJANGO_SETTINGS_MODULE=settings.local ./env/bin/python app/manage.py makemigrations
	DJANGO_SETTINGS_MODULE=settings.local ./env/bin/python app/manage.py migrate
	DJANGO_SETTINGS_MODULE=settings.local ./env/bin/python app/manage.py syncdb
	@echo "Migrations in development applied..."


cleancache:
	rm -rf var/cache/*
	rm -rf public/media/cache/*

env:
	virtualenv env

bin:
	mkdir -p bin

var:
	mkdir -p var/cache
	mkdir -p var/log
	mkdir -p var/db
	mkdir -p var/run

dev_requirements:
	./env/bin/pip install -r requirements/development.txt

prod_requirements:
	./env/bin/pip install -r requirements/production.txt

static:
	$(info - Collect static files and process them for production use)
	mkdir -p public/static
	mkdir -p public/media

	./env/bin/python app/manage.py collectstatic \
	         -v 0 \
	         --noinput \
	         --traceback \
	         -i django_extensions \
	         -i '*.coffee' \
	         -i '*.rb' \
             -i '*.scss' \
	         -i '*.less' \
	         -i '*.sass'

deps:
	$(info - Installing all system dependencies using apt-get)
	$(call getdeb, build-essential)
	$(call getdeb, python-setuptools)
	$(call getdeb, python-pip)
	$(call getdeb, python-virtualenv)
	$(call getdeb, python-dev)
	$(call getdeb, rpl)
	$(call getdeb, zip)
	$(call getdeb, postgresql)
	$(call getdeb, postgresql-contrib)
	$(call getdeb, libpq-dev)


server:
	@echo "Open your browser at localhost:5000"
	DJANGO_SETTINGS_MODULE=settings.local ./env/bin/python app/manage.py runserver 0.0.0.0:5000

html:
	cd docs && make html

live:
	cd docs && make live

clean_template:
	rm -rf template

template: clean_template
	mkdir -p template
	tar -zcf template.tar.gz -T config/template.files -X config/ignored.files
	tar -zxvf template.tar.gz -C template
	rm template.tar.gz
	rpl -R {{ project_name }} {{\ project_name\ }} template/
	zip -r template.zip template/* template/.gitignore
	rm -r template


NAME="{{ project_name }}_project"
project: template
	cd .. && mv $(CURDIR)/template.zip . && \
	django-admin.py startproject \
		--template template.zip \
		--extension py,rst,md,ini,* $(NAME) && \
    rm template.zip
	@echo
	@echo ----------------------------------------------------------------------
	@echo "Project <<$(NAME)>> created. :)"
	@echo ----------------------------------------------------------------------

