#!/bin/sh

echo "Migrating the databse..."
python manage.py migrate

echo "Starting the server..."
python manage.py runserver 0.0.0.0:80