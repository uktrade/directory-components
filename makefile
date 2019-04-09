build: test_requirements test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -e .[test]

flake8:
	flake8 . --exclude=.venv,setup.py,directory_components/version.py,node_modules

pytest:
	pytest . --ignore=node_modules --cov=. --cov-config=.coveragerc $(pytest_args) --capture=no -vv --last-failed --cov-report=html

CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test: flake8 pytest
	$(CODECOV)

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
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007/; \
	export DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL=http://international.trade.great:8012/international/; \
	export INVEST_BASE_URL=http://invest.trade.great:8012/


DJANGO_WEBSERVER := \
	./manage.py collectstatic --noinput --settings=demo.config.settings && \
	./manage.py runserver --settings=demo.config.settings 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

run_demo:
	$(DEMO_SET_ENV_VARS) && $(DJANGO_WEBSERVER)


.PHONY: build clean test_requirements flake8 pytest test publish
