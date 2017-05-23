#!/bin/sh
cd src

until nc -z -v -w30 mysql 3306
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

if [ "$DJANGO_IS_DEBUG" = "" ]
then
   echo "Starting production server..."
   /usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app/src
else
   echo "Starting development server..."
   python3 manage.py runserver_plus 0.0.0.0:8000
fi
