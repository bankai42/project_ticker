FROM python:3.11-slim

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY requirements.txt /app/
# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ticker.wsgi:application"]
