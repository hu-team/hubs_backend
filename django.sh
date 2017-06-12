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

if [ "$DJANGO_IS_CELERY" = "1" ]
then
    # Let the app run migrations first.
    sleep 10

    # Start celery worker.
    celery -A celeryApp worker -B -l info $@
else
    # Execute migrations
    python3 manage.py migrate --noinput

    # Collect static files.
    python3 manage.py collectstatic --noinput

    # Start server.
    if [ "$DJANGO_IS_DEBUG" = "0" ]
    then
       echo "Starting production server..."
       /usr/local/bin/gunicorn config.wsgi -w 6 -b 0.0.0.0:8000 --chdir=/app/src $@
    else
       echo "Starting development server..."
       while true; do
          python3 manage.py runserver_plus 0.0.0.0:8000 $@
       done
    fi
fi
