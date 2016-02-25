# PROJECT_CORE

Core for django project.
========================

### INSTALLATION ###


!!! REQUIREMENTS !!!

1. Apt-get requirements:
    sudo apt-get update
    sudo apt-get install curl python-pip git-all screen libpq-dev libev4 python-dev libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk Nginx openjdk-7-jre fabric

2. Postgres >= 9.5
3. Redis
4. ElasticSearch >= 2.2

!!! END REQUIREMENTS !!!


!!! REPOSITORY CHANGES !!!

1. Clone git repository

2. Rename directories and files from 'project_core' to project name:
    -main project directory
    -django/project_core/
    -project_core.py

3. Replace 'project_core' in all files with project name

4. Create settings/local.py file using local_example.py

5. mkvirtualenv && pip install -r requirements/requirements_development.txt

6. make makemigrations && make migrate

7. Rewrite this README.md

!!! END REPOSITORY CHANGES !!!
### END INSTALLATION ###


### GETTING STARTED ###

Create new app:
    - ./manage.py startapp new_app
    - move new_app directory to apps/
    - add app_name to settings/_apps.py
    - [add urls namespace to urls/urls.py]

Templates creation:
    - create template/app_name/new_template.jinja2 in apps/app_name/ directory


### END GETTING STARTED ###
