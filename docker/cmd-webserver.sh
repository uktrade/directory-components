#!/bin/bash -xe

python /usr/src/app/manage.py collectstatic --noinput
gunicorn demo.config.wsgi --bind 0.0.0.0:$PORT
