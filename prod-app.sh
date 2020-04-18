#!/usr/bin/env bash
set -x
cd /app/h42-auth
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile- h42auth:app
