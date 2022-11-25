django = docker-compose exec django ./manage.py

migrate:
	sh -c "$(django) migrate --noinput"

makemigrations:
	sh -c "$(django) makemigrations"

createsuperuser:
	sh -c "$(django) createsuperuser"

collectstatic:
	sh -c "$(django) collectstatic"

shell:
	sh -c "$(django) shell"