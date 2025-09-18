#!/bin/bash

echo "Iniciando DynoIA Container..."

# Start nginx for frontend
nginx -g "daemon off;" &

# Start backend
cd /app/backend
python main.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
