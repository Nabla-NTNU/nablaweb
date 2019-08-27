#!/bin/bash

# Remember to run as user nablaweb

cd /srv/nablaweb
pipenv run python manage.py update_index
