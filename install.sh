#!/bin/bash

# Set the domain and location variables
read -p "Enter domain to retrieve SSL certs for: " domain
read -p "Enter directory to store SSL certs: " location

image="porkcert"
# Check if the Docker image exists and build if not
if ! docker image inspect "$image" &> /dev/null; then
  echo "Building $image docker image..."
  docker build -t "$image" . > /dev/null 2>&1
  echo "Finished building $image"
fi

cmd="docker run -v $HOME/.config/:/root/.config --name porkcert-cron -v $location:$location $image -d $domain -l $location"

# Run once
$cmd
echo "Installed certs to $location"

if ! command -v crontab &> /dev/null; then
  echo "Error: cron is not installed. Cannot set up job to maintain porkbun certs"
  exit 1
fi

# Update daily cron schedule
cronsched="0 0 * * *"

# Set docker run job as crontab job if doesn't exist
if (crontab -l 2>/dev/null | grep -q -F "$cmd"); then
  echo "Cron job already exists. Skipping installation."
else
  if crontab -l &> /dev/null; then
    (crontab -l ; echo "$cronsched $cmd") | crontab -
    echo "Scheduled job to update daily (check with crontab -e)"
  else
    echo "$cronsched $cmd" | crontab -
    echo "New crontab job created to keep certs updated"
  fi
fi
