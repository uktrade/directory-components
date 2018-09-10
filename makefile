build: test_requirements test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

flake8:
	flake8 . --exclude=.venv,setup.py,directory_components/version.py

pytest:
	pytest . --cov=. --cov-config=.coveragerc $(pytest_args) --capture=no -vv --last-fail

CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test: flake8 pytest
	$(CODECOV)

DOCKER_SET_ENV_VARS := \
	export DIRECTORY_COMPONENTS_SECRET_KEY=debug; \
	export DIRECTORY_COMPONENTS_DEBUG=true; \
	export DIRECTORY_COMPONENTS_PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_COMPONENTS_PORT=9000; \
	export DIRECTORY_COMPONENTS_HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export DIRECTORY_COMPONENTS_HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/

publish:
	rm -rf build dist; \
	python setup.py bdist_wheel; \
	twine upload --username $$DIRECTORY_PYPI_USERNAME --password $$DIRECTORY_PYPI_PASSWORD dist/*

update:
	bash ./scripts/header_footer_git_make_branch.sh
	python ./scripts/upgrade_header_footer.py
	bash ./scripts/header_footer_git_push_changes.sh


DEMO_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export DEBUG=true; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export PORT=9013; \
	export HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/; \
	export INVEST_BASE_URL=http://invest.trade.great:8012/

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f ./docker-compose.yml rm -f && docker-compose -f ./docker-compose.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_ENV_VARS := \
	export DIRECTORY_COMPONENTS_SECRET_KEY=debug; \
	export DIRECTORY_COMPONENTS_DEBUG=false; \
	export DIRECTORY_COMPONENTS_PORT=9000; \
	export DIRECTORY_COMPONENTS_HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export DIRECTORY_COMPONENTS_HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/; \
	export DIRECTORY_COMPONENTS_INVEST_BASE_URL=http://invest.trade.great:8012/


docker_test_env_files:
	$(DOCKER_SET_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep directoryui_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_webserver_bash:
	docker exec -it directoryui_webserver_1 sh

docker_build:
	docker build -t ukti/directory-components:latest .

heroku_deploy_dev:
	./docker/install_heroku_cli.sh
	docker login --username=$$HEROKU_EMAIL --password=$$HEROKU_TOKEN registry.heroku.com
	~/bin/heroku-cli/bin/heroku container:push web --app directory-components-dev
	~/bin/heroku-cli/bin/heroku container:release web --app directory-components-dev

DJANGO_WEBSERVER := \
	./manage.py collectstatic --noinput --settings=demo.config.settings && \
	./manage.py runserver --settings=demo.config.settings 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

run_demo:
	$(DEMO_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

docker_webserver: docker_remove_all
	$(DOCKER_SET_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose build && \
	docker-compose run --service-ports demo make django_webserver

.PHONY: build clean test_requirements flake8 pytest test publish
