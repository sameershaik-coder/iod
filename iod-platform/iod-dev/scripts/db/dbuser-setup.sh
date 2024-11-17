#!/bin/bash

iod_env=$1

echo "env param sent to db script is: $iod_env"

cd /home/ioduser/stockodiary2/
source .env

echo "db username is : $DB_USER"
echo "db password is : $DB_PASSWORD"

# Check if param1 is equal to "dev".
if [ "$iod_env" == "dev" ]; then
    echo "param1 is equal to dev"
    echo "Altering db user permissions"
    sudo -u postgres psql -p 5433 -v ON_ERROR_STOP=1 -e  <<EOF
    ALTER USER postgres WITH PASSWORD 'Test@123';
    EOF

    sudo -u postgres psql -p 5433 -v ON_ERROR_STOP=1 -e  <<EOF
    CREATE DATABASE sdiarydos;
    EOF

    sudo -u postgres psql -p 5433 -v ON_ERROR_STOP=1 -e  <<EOF
    GRANT ALL PRIVILEGES ON DATABASE sdiarydos TO postgres;
    EOF
else
    echo "param1 is not equal to dev"
    echo "Altering db user permissions"
    sudo -u postgres psql -v ON_ERROR_STOP=1 -e  <<EOF
    ALTER USER postgres WITH PASSWORD 'Test@123';
    EOF

    sudo -u postgres psql -v ON_ERROR_STOP=1 -e  <<EOF
    CREATE DATABASE sdiarydos;
    EOF

    sudo -u postgres psql -v ON_ERROR_STOP=1 -e  <<EOF
    GRANT ALL PRIVILEGES ON DATABASE sdiarydos TO postgres;
    EOF
fi

