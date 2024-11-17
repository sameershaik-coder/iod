#!/bin/sh

# Check if $1 is not null
if [ -n "$1" ]
then
  # If $1 is not null, assign it to a variable
  first_param=$1
  echo "Provided environment is : - $first_param"
else
  echo "No parameter provided. Please provide a parameter."
  first_param="dev"
fi


iod_env=$first_param

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
# Move env file into repo created above
cp .env stockodiary2/

sudo apt-get update
sudo apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
sudo apt install python3.10-venv

cd /home/ioduser/infra/db/
#"$(dirname "$0")/somedb.sh"
sudo bash ./dbuser-setup.sh $iod_env

#sudo apt install python3.11-venv -y

cd /home/ioduser/stockodiary2/

python3 -m venv .venv

mkdir logs

cd /home/ioduser/

"$(dirname "$0")/iod-stage2.sh"

"$(dirname "$0")/start-server.sh"

cd /home/ioduser/
