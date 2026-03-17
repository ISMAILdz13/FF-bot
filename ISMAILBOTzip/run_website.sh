#!/bin/bash
# Start ISMAIL Website with auto-restart functionality
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting ISMAIL Website with auto-restart..."
while true; do
    echo "[$(date)] Starting website..."
    cd "$SCRIPT_DIR" && python3 website/app.py
    EXIT_CODE=$?
    echo "[$(date)] Website exited with code $EXIT_CODE. Restarting in 5 seconds..."
    sleep 5
done
