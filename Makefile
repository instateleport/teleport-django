django = docker-compose exec django ./manage.py

migrate:
	sh -c "$(django) migrate --noinput"

makemigrations:
	sh -c "$(django) makemigrations"

collectstatic:
	sh -c "$(django) collectstatic"