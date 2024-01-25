#!/bin/bash

CheckCommand()
{
   $*
   if [ $? -ne 0 ]; then
      echo "Error occured. Aborting."
      exit 1
   fi
}

CheckForSudo()
{
   if [[ $EUID -ne 0 ]]; then
      echo "Needs root." 
      exit 1
   fi 
}

UpdateApt()
{
   CheckCommand apt-get update -qq -y
}

InstallRequiredPackages()
{
   REQUIRED_PACKAGES="python3-pip net-tools iproute2"
   CheckCommand apt-get install -qq -y ${REQUIRED_PACKAGES}
}

InstallRequiredPipPackages()
{
   CheckCommand pip install -r -q requirements.txt
}

Main()
{
   echo "Running setup for spoofer"
   CheckForSudo
   echo "-> Updating apt repo..."
   UpdateApt
   echo "-> Installing apt packages..."
   InstallRequiredPackages
   echo "-> Installing pip packages..."
   InstallRequiredPipPackages
   echo "Setup completed successfully!"
}

Main