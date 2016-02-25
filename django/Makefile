TEST_APPLICATIONS=account

run:
	python manage.py runserver_plus

shell:
	python manage.py shell_plus --print-sql

notebook_shell:
	python manage.py shell_plus --notebook

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

makedatamigration:
	python manage.py makemigrations --empty $(app)

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;

celery:
	celery worker -A project_core -B

test:
	python manage.py test $(TEST_APPLICATIONS)
