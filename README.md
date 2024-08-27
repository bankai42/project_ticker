
# Ticker

A simple web-app for creatint tickers online.
Ticker - is a running string with some text.




## Deployment

To deploy this project clone this repository. Create and activate virtual environment and install requirements.

```bash
  python -m venv venv
```
Windows
```bash
  source venv/Scripts/activate
  pip install -r requirements.txt
```
Linux
```bash
  source venv/bin/activate
  pip install -r requirements.txt
```

Migrate database
```bash
  python manage.py migrate
```
Run the application
```bash
  python manage.py runserver
```


## API Reference

#### Get all users

```http
  GET /api/users
```

#### Get user

```http
  GET /api/user/{id}
```

#### Get all tickers

```http
  GET /api/tickers
```

#### Get ticker

```http
  GET /api/ticker/{id}
```

