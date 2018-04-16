#!/bin/bash

cd /srv/nablaweb
source venv/bin/activate
source /etc/websites/nablaweb/gunicorn.conf
./venv/bin/python manage.py update_index
