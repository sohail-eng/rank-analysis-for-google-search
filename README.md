# Rank Analysis for Google Search

A Django-based web application that analyzes and tracks Google search rankings for specific websites and keywords. This tool helps SEO professionals, digital marketers, and website owners monitor their search engine positioning by providing real-time ranking data through an asynchronous API.

## Features
- **Asynchronous Google Search Analysis**: Uses Celery workers to process ranking requests in the background
- **Proxy Support**: Implements proxy rotation to avoid rate limiting and IP blocking
- **RESTful API**: Provides endpoints for submitting ranking analysis requests and retrieving results
- **Swagger Documentation**: Interactive API documentation for easy testing and integration
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Real-time Monitoring**: Flower dashboard for monitoring Celery task progress

## How It Works
1. Submit a URL and list of keywords to analyze
2. The system searches Google for each keyword using proxy rotation
3. Tracks the position of your website in search results
4. Returns ranking data asynchronously via task ID
5. Monitor task progress and retrieve final results

## Clone Repository:
```shell
https://github.com/sohail-eng/rank-analysis-for-google-search
```

## Docker Setup
### Create `.env` file
```shell
cp .env.docker .env
```
Add values of requirement variables in `.env` file.

### Start Docker container
```shell
docker-compose up --build -d
```
### Create superuser
```shell
sudo docker exec -it rank-analysis-for-google-search_web_1 bash
python manage.py createsuperuser
exit
```

## Setting up Local Environment
### Create virtual environment
```shell
python -m venv venv
```

### Activate virtual environment
```shell
source venv/bin/activate
```

### Install requirements
```shell
./setup.sh
```

### Create `.env` file
```shell
cp .env.sample .env
```
Add values of requirement variables in `.env` file.

### Make migrations
```shell
python manage.py migrate
```

### Start app
```shell
python manage.py runserver
```

### Create superuser (local)
```shell
python manage.py createsuperuser
```

### Start celery worker
```shell
celery -A rank_analysis.celery_services.celery_services.celery_app worker --loglevel=INFO
```

### Swagger Documentation
[swagger](http://127.0.0.1:8000/swagger/)

### Flower
[flower](http://127.0.0.1:5555/)
