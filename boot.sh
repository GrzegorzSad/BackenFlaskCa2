#!/bin/bash
sleep 2
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
echo _-_ db created _-_
flask seed-db
echo _-_ db seeded _-_
exec gunicorn -b :8000 --access-logfile - --error-logfile - server:app