#!/bin/bash


path=$(pwd)
cd ..
clear

if [ -f "$path/.env" ]; then
    set -a  
    source "$path/.env"
    set +a
else
    echo "Error: .env file not found."
    exit 1
fi

if [ ! -f "$path/.venv/bin/python" ]; then
    echo "Error: Virtual environment not found in $path/.venv"
    exit 1
fi

echo -e "\n\nStarting DisSafe Shield API\n\n"
"$path/.venv/bin/python" "$path/manage.py" runserver "$HOST:$PORT"
echo -e "\n\n"
