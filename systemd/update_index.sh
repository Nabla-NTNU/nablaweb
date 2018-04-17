#!/bin/bash

cd /srv/nablaweb
source venv/bin/activate
source /etc/websites/nablaweb/config.env
./venv/bin/python manage.py update_index
