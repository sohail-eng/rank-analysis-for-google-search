FROM python:3.8.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/
COPY requirements-dev.txt /app/

RUN pip install --upgrade pip

RUN rm -rf /root/.cache/pip

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
