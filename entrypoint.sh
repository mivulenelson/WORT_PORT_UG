#!/bin/bash

# collect static files
echo "collect static files"
python manage.py collectstatic --noinput

# apply database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# execute the commands
exec "$@"