build: test_requirements test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

flake8:
	flake8 . --exclude=.venv,setup.py,directory_components/version.py

pytest:
	pytest . --cov=. --cov-config=.coveragerc $(pytest_args) --capture=no

CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test: flake8 pytest
	$(CODECOV)

compile_requirements:
	python3 -m piptools compile requirements.in

compile_test_requirements:
	python3 -m piptools compile requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

DEMO_SET_ENV_VARS := \
	export HEADER_FOOTER_URLS_CONTACT_US=http://contact.trade.great:8009/directory/; \
	export HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/

run_demo:
	$(DEMO_SET_ENV_VARS) && ./manage.py collectstatic --noinput --settings=demo.settings && ./manage.py runserver --settings=demo.settings 0.0.0.0:9000

publish:
	rm -rf build dist; \
	python setup.py bdist_wheel; \
	twine upload --username $$DIRECTORY_PYPI_USERNAME --password $$DIRECTORY_PYPI_PASSWORD dist/*

update:
	bash ./scripts/header_footer_git_make_branch.sh
	python ./scripts/upgrade_header_footer.py
	bash ./scripts/header_footer_git_push_changes.sh

.PHONY: build clean test_requirements flake8 pytest test publish
