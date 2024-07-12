#!/bin/bash
source /var/www/shahzodspace/venv/bin/activate
exec gunicorn shahzod_space.wsgi:application -c gunicorn_config.py
