FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat dos2unix

ADD requirements.txt /app/requirements.txt
ADD django.sh /django.sh
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN dos2unix /django.sh && chmod +x /django.sh
CMD [ "/django.sh" ]

EXPOSE 8000
