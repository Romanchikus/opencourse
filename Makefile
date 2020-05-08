start:
	pip install -r requirements/local.txt
	./manage.py makemigrations
	./manage.py migrate
	./manage.py loaddata tmp/course_help_data.json

restart:
	rm tmp/db.sqlite3 -f
	find opencourse/courses/migrations/ -name '00*.py' -delete
	find opencourse/profiles/migrations/ -name '00*.py' -delete
	pip install -r requirements/local.txt
	./manage.py makemigrations
	./manage.py migrate
	./manage.py loaddata tmp/course_help_data.json
