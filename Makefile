start_local:
	pip install -r requirements/local.txt
	./manage.py loaddata tmp/course_help_data.json
	./manage.py makemigrations
	./manage.py migrate
