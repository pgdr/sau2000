#!/bin/bash
SETTINGS=${DJANGO_SETTINGS_MODULE:-sausite.settings}

rm /etc/nginx/sites-enabled/default
ln -s /configs/nginx.conf /etc/nginx/sites-enabled/sau

/etc/init.d/nginx restart

echo Starting Gunicorn.
echo Using settings $SETTINGS
exec gunicorn --env DJANGO_SETTINGS_MODULE=$SETTINGS sausite.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 3
