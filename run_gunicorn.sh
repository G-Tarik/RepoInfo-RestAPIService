#!/bin/sh

exec gunicorn --bind '0.0.0.0:7000' --workers 4 --worker-class gevent \
              --access-logfile - --error-logfile - "app:create_app()"
