#!/bin/bash -e

# Check for administrative privileges
if [[ $EUID -ne 0 ]]; then
   echo "Needs root." 
   exit 1
fi

REQUIRED_PACKAGES="git python3-pip net-tools iproute2"

echo "Running setup for spoofer"
apt-get update
apt-get install $REQUIRED_PACKAGES -y
pip install -r requirements.txt
echo "Setup completed."