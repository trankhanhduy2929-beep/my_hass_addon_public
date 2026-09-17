#!/usr/bin/with-contenv bashio
exec gunicorn --bind 0.0.0.0:2032 --worker-class gthread --workers 1 --threads 16 --timeout 0 --keep-alive 10 --no-control-socket --access-logfile - --error-logfile - app:app
