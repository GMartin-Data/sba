#!/bin/sh

# Effectuer les migrations
echo "Effectuer les migrations de la base de données..."
python manage.py makemigrations && python manage.py migrate

python manage.py runserver 0.0.0.0:8000