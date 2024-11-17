#!/bin/bash

cd /home/ioduser/stockodiary2
source .venv/bin/activate
pip install -r requirements.txt


python manage.py migrate

python manage.py collectstatic

sudo locale-gen en_IN

sudo locale-gen en_IN.UTF-8

sudo update-locale

cd  /home/ioduser/infra/

sudo ./stop-server.sh

chmod +x setup-gunicorn.sh

sudo ./setup-gunicorn.sh

sudo ./setup-nginx.sh

sudo nginx -t

sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'

sudo systemctl status nginx

sudo ./start-server.sh


