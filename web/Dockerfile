FROM python:3.11-slim

WORKDIR /web

COPY requirements.txt .

RUN python -m venv venv

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /web/

EXPOSE 8080

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver"]