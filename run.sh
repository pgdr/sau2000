#!/bin/bash

SETTINGS=${DJANGO_SETTINGS_MODULE:-sausite.settings}

echo $PYTHONPATH
echo Starting Gunicorn.
echo Using settings $SETTINGS
exec gunicorn --env DJANGO_SETTINGS_MODULE=$SETTINGS sausite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3