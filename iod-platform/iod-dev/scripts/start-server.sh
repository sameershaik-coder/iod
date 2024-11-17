#!/bin/bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo ln -s /etc/nginx/sites-available/stockodiary2 /etc/nginx/sites-enabled
sudo systemctl status gunicorn