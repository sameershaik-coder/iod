#!/bin/sh
set -e

iod_env="master"

sudo apt -y update

if git --version >/dev/null 2>&1;
then
        echo "git is already installed"

else
        echo "Git is not installed. Installing now..."
        sudo apt-get -y update
        sudo apt-get install git -y
fi

repo_url="git@github.com:sameershaik-coder/stockodiary2"
echo "repo url  is $repo_url"
repo_dir=$(basename -s .git "$repo_url")
if [ -d "$repo_dir" ]; then
        echo "Git repository: $repo_dir already exists"
else
        echo "Git repository does not exist. Cloning now..."

        git clone --branch $iod_env "$repo_url"
fi
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
sudo apt install python3.10-venv

# Copy env file to repo directory
cd /home/ioduser

cp .env stockodiary2/

REPO_DIR=/home/ioduser/stockodiary2/


if [ -f "$REPO_DIR/.env" ]; then
    echo "Environment File copied successfully."
else
    echo "Failed to copy file Environment."
    exit 1
fi

cd /home/ioduser/stockodiary2/

python3 -m venv .venv

mkdir logs

cd /home/ioduser/

"$(dirname "$0")/iod-stage2.sh"

"$(dirname "$0")/start-server.sh"

