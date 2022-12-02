django = docker-compose exec django ./manage.py

migrate:
	sh -c "$(django) migrate $(ARGS)"

makemigrations:
	sh -c "$(django) makemigrations $(ARGS)"

createsuperuser:
	sh -c "$(django) createsuperuser"

collectstatic:
	sh -c "$(django) collectstatic"

shell:
	sh -c "$(django) shell"

startapp:
	sh -c "$(django) startapp $(APPNAME)"