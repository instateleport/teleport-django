django = docker-compose -f docker-compose.dev.yml exec web ./manage.py

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