#!/bin/bash

cd /home/ioduser/stockodiary2/
source .env
echo $SERVER
export IP_ADDRESS=$SERVER

cd /home/ioduser/infra/lib/
envsubst < stockodiary2 > /etc/nginx/sites-available/stockodiary2

