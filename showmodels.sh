#!/bin/bash
now=$(date +"%Y_%m_%d")
python manage.py showmodels 2> $now.dat
