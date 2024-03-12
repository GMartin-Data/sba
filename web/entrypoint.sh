#!/bin/sh

# Effectuer les migrations
echo "Effectuer les migrations de la base de données..."
python manage.py makemigrations && python manage.py migrate

echo "Collecter les fichiers statiques"
python manage.py collectstatic --no-input

echo "Lancer le serveur"
# Prod
# gunicorn project.wsgi:application --workers=4 --timeout 120 --bind=0.0.0.0:8000
# Dev
python manage.py runserver 0.0.0.0:8000