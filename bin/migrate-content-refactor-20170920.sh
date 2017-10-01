#!/usr/bin/env bash
# Script to migrate the production database after content-refactor
# it can safely be removed some time after it has been run

# Remember:
# 	* run migrate-content-refactor-20170920.sql first.
# 	* Run this script in virtualenv

python manage.py migrate news 0001_initial --fake
python manage.py migrate events 0001_initial --fake
python manage.py migrate album 0001_initial --fake
python manage.py migrate blog 0001_initial --fake
python manage.py migrate image 0001_initial --fake

python manage.py migrate

