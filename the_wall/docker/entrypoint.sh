#!/bin/sh

echo "Waiting for mongodb..."

while ! nc -z mongo 27017; 
do
	sleep 0.1
done
echo "Mongodb started"

python /app/create_admin_data.py
python /app/main.py
exec "$@"
