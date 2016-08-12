#!/bin/bash

dropdb py-ferry
createdb py-ferry
python manage.py importdata
python manage.py adduser
python manage.py run