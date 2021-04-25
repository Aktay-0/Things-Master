#!/bin/bash
cd /var/repos/thigs-master/Things-Master/.env/  #path to virtual environment
. bin/activate  #Activate virtual environment
cd /var/repos/thigs-master/Things-Master/gsm_manager/ #path to django project
python3 manage.py runserver 0:8090 #run django server

