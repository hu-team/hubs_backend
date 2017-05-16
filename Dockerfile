FROM python:3.6

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "/app/django.sh" ]

EXPOSE 8000
