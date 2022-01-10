#!/bin/sh
python manage.py migrate --noinput
python manage.py loaddata initial_data.json
python manage.py collectstatic --no-input --clear

exec "$@"