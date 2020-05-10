start:
	pip install -r requirements/local.txt
	./manage.py makemigrations
	./manage.py migrate
	./manage.py loaddata tmp/course_help_data.json

reset:
	rm scripts/db.sqlite3 -f
	find opencourse/courses/migrations/ -name '00*.py' -delete
	find opencourse/profiles/migrations/ -name '00*.py' -delete
	pip install -r requirements/local.txt
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runscript 2020_05_10_2
	./manage.py runscript 2020_05_10

translate:
	./manage.py makemessages -i venv -i */account
	./manage.py compilemessages -i venv -l ru

dumpdb:
	./manage.py dumpscript courses profiles account.EmailAddress > scripts/2020_05_10.py
