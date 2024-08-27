
# Ticker

A simple web-app for creating tickers online.
Ticker - is a running string with some text.




## Deployment

To deploy this project clone this repository. Create and activate virtual environment and install requirements.

```bash
  python3 -m venv venv
```
Windows
```bash
  source venv/Scripts/activate
  pip install -r requirements.txt
```
Linux
```bash
  apt-get update
  apt-get -y install libpq-dev gcc
  source venv/bin/activate
  pip install psycopg2
  pip install -r requirements.txt
```

Migrate database
```bash
  python3 manage.py migrate
```
Run the application
```bash
  python3 manage.py runserver
```


## API Reference

#### Get all users

```http
  GET /api/users
```

#### Get user

```http
  GET /api/users/{id}
```

#### Get all tickers

```http
  GET /api/tickers
```

#### Get ticker

```http
  GET /api/tickers/{id}
```

