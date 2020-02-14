#!/usr/bin/env bash
if python3 /app/admin/manage.py makemigrations ; then
    python3 /app/admin/manage.py migrate
    cd cd /app/admin/ && /usr/local/bin/gunicorn --workers=4 --max-requests=1000 --timeout 4000 -c gunicorn.py admin.wsgi
fi
