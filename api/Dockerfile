FROM python:3.11-slim

WORKDIR /api

COPY requirements.txt /api

RUN python -m venv venv

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /api/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]