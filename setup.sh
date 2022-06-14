#!/bin/bash

# Check for administrative privileges
if [[ $EUID -ne 0 ]]; then
   echo "Needs root." 
   exit 1
fi

# Print information
PROGRAM_VERSION="0.0.2"
echo "Running setup for spoofer $PROGRAM_VERSION"