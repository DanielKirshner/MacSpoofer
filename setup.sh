#!/bin/bash -e

# Check for administrative privileges
if [[ $EUID -ne 0 ]]; then
   echo "Needs root." 
   exit 1
fi

###### Constants ######
PROGRAM_VERSION="0.0.2"
REQUIRED_PACKAGES="git python3-pip net-tools iproute2"
#######################

echo "Running setup for spoofer $PROGRAM_VERSION"
apt-get update
apt-get install $REQUIRED_PACKAGES -y
git clone https://github.com/DanielKirshner/MacSpoofer
pip install -r MacSpoofer/requirements.txt
echo "Setup completed."
