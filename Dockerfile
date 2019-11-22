FROM python:3.8.0-alpine3.10

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

EXPOSE 80

WORKDIR /data
COPY ./api /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:api"]
