#!/bin/bash

# specify the target directory and filename
target_directory="/etc/systemd/system/"
filename="gunicorn.service"

# full path of the file
file_path="${target_directory}/${filename}"

# check if file exists
if [ -f "$file_path" ]
then
    echo "File $file_path exists."
    # delete the file
    rm "$file_path"
    echo "File $file_path deleted."
else
    echo "File $file_path does not exist."
fi

# copy the file from current directory to target directory
sudo cp "/home/ioduser/stockodiary2/scripts/lib/${filename}" "$target_directory"
echo "File ${filename} copied from current directory to $target_directory."
