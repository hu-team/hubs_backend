#!/bin/sh
cd /app/src

until nc -z -v -w30 mysql 3306
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

until nc -z -v -w30 rabbitmq 5672
do
  echo "Waiting for broker connection..."
  # wait for 5 seconds before check again
  sleep 5
done

python3 manage.py migrate --noinput

if [ "$DJANGO_IS_CELERY" = "1" ]
then
    # Start celery worker.
    celery -A celeryApp worker -B -l info $@
else
    # Collect static files.
    python3 manage.py collectstatic --noinput

    # Start server.
    if [ "$DJANGO_IS_DEBUG" = "0" ]
    then
       echo "Starting production server..."
       /usr/local/bin/gunicorn config.wsgi -w 6 -b 0.0.0.0:8000 --chdir=/app/src $@
    else
       echo "Starting development server..."
       python3 manage.py runserver_plus 0.0.0.0:8000 $@
    fi
fi
