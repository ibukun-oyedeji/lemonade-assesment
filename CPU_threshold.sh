#!/bin/bash

# Set threshold for CPU usage
CPU_THRESHOLD=80

# Get the process ID (PID) of the Laravel backend service
# Replace "php artisan queue:work" with the actual command used to start your service
PID=$(pgrep -f "php artisan queue:work")

while true; do
  # Get current CPU usage of the process
  CPU_USAGE=$(top -b -n 1 -p $PID | tail -n +8 | awk '{print $9}')

  # Check if CPU usage exceeds the threshold
  if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    echo "CPU usage exceeds $CPU_THRESHOLD%. Restarting Laravel service..."

    # Stop the Laravel service
    # Replace with the appropriate command to stop your service gracefully
    # For example: php artisan queue:restart
    php artisan queue:restart

    echo "Laravel service restarted."
  fi

  # Wait for a specified interval before checking again
  sleep 60 
done
