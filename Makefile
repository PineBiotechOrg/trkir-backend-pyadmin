init:
	pip3 install -r requirements.txt

precommit_init:
	pip3 install pre-commit
	pre-commit install

start:
	python3 admin/manage.py runserver 0.0.0.0:8061

init_n_start:
	make init
	make precommit_init
	make start

make_migrations:
	python3 admin/manage.py makemigrations "$(PROJECT)"

sqlmigration:
	python3 admin/manage.py sqlmigrate "$(PROJECT)" "$(VERSION)"

migrate:
	python3 admin/manage.py migrate

shell:
	python3 admin/manage.py shell

lint:
	pylint admin/

build_docker:
	bash scripts/build.sh
