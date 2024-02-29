FROM python:3.11-slim

WORKDIR /web

COPY requirements.txt .

RUN python -m venv venv

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /web/

EXPOSE 8000

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]