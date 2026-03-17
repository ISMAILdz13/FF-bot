#!/bin/bash
# Start ISMAIL-BOT with auto-restart functionality
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting ISMAIL-BOT with auto-restart..."
while true; do
    echo "[$(date)] Starting bot process..."
    cd "$SCRIPT_DIR" && python3 ISMAIL_BOT/main.py
    EXIT_CODE=$?
    echo "[$(date)] Bot exited with code $EXIT_CODE. Restarting in 5 seconds..."
    sleep 5
done
