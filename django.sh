#!/bin/sh
cd src

sleep 3

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput && /usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app/src
