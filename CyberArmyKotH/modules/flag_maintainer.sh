#!/bin/bash
# ==============================================================================
# CYBERARMY V10.8 - SAFE FLAG MAINTAINER
# ==============================================================================

FLAG_PATH="/var/www/html/flag.txt"
TEAM_ID="CyberArmy_V10_8"
SLEEP_INTERVAL=5

echo "[+] [Bash Maintainer] Bắt đầu duy trì flag với chu kỳ ${SLEEP_INTERVAL}s..."

while true; do
    if [ -w "$FLAG_PATH" ]; then
        printf "%s\n" "$TEAM_ID" > "$FLAG_PATH"
    fi
    sleep "$SLEEP_INTERVAL"
done
