Project Name : Bella [proposed name : stockodiary2]
Version : 1.0
End Date : 19-04-2024
Status : Closed/Completed
## docker commands
docker build -t iod_app .
sudo docker ps -a
htop
docker compose up -d --build

http://139.59.65.182:8000/app/networth/upload

## vs code launch.json

### iod-web single
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Web",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "django": true,
            "justMyCode": true,
            "autoStartBrowser": false,
            "python": "${workspaceFolder}/.webenv/bin/python",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        },
        
    ]
}


### combined
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/iod-web/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "django": true,
            "justMyCode": true,
            "autoStartBrowser": false,
            "python": "${workspaceFolder}/iod-web/.webenv/bin/python",
            "cwd": "${workspaceFolder}/iod-web",
            "console": "integratedTerminal"
        },
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload",
                "--port",
                "5002",
            ],
            "jinja": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}/pdffusion"
            }
        },
    ]
}


## droplet setup
droplet -2 
-------------------------------
ssh root@165.22.215.81

ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE sdiarydos TO postgres;

ALTER USER postgres WITH PASSWORD 'Test@123';
\du

sudo apt install redis-server

celery -A core.settings_templates worker -l info

celery -A core.settings_templates flower

http://localhost:5555/broker

redis-server

sudo service redis-server start

redis-cli ping

https://sameershaik19.atlassian.net/wiki/spaces/S/pages/153223171/6.0+Expose+postgresql+server+access

hello test
