#!/bin/bash

CheckCommand()
{
   $*
   if [ $? -ne 0 ]; then
      echo "Error occurred. Aborting."
      exit 1
   fi
}

# Run a command as the original (non-root) user who invoked sudo.
# Uses ORIGINAL_USER resolved by ResolveOriginalUser().
RunAsUser()
{
   su "${ORIGINAL_USER}" -c "$*"
   if [ $? -ne 0 ]; then
      echo "Error occurred. Aborting."
      exit 1
   fi
}

# Resolve the actual non-root user. $SUDO_USER may be empty on some distros
# (e.g. Bazzite), so fall back to logname which reads from the TTY.
ResolveOriginalUser()
{
   ORIGINAL_USER="${SUDO_USER:-$(logname 2>/dev/null)}"
   if [ -z "${ORIGINAL_USER}" ]; then
      echo "Could not determine the original user. Run with sudo from a regular user account."
      exit 1
   fi
   echo "-> Running brew commands as user: ${ORIGINAL_USER}"
}

CheckForSudo()
{
   if [[ $EUID -ne 0 ]]; then
      echo "Needs root."
      exit 1
   fi
}

DetectPackageManager()
{
   if command -v apt-get &>/dev/null; then
      PKG_MANAGER="apt"
   elif command -v brew &>/dev/null; then
      PKG_MANAGER="brew"
   elif command -v dnf &>/dev/null; then
      PKG_MANAGER="dnf"
   else
      echo "Unsupported package manager. Only apt, brew, and dnf are supported."
      exit 1
   fi
   echo "-> Detected package manager: ${PKG_MANAGER}"
}

UpdateRepos()
{
   if [ "${PKG_MANAGER}" = "apt" ]; then
      CheckCommand apt-get update -qq -y
   elif [ "${PKG_MANAGER}" = "brew" ]; then
      RunAsUser brew update -q
   else
      CheckCommand dnf check-update -q --refresh || true  # dnf returns exit code 100 when updates are available
   fi
}

InstallRequiredPackages()
{
   if [ "${PKG_MANAGER}" = "apt" ]; then
      REQUIRED_PACKAGES="python3-pip net-tools iproute2"
      CheckCommand apt-get install -qq -y ${REQUIRED_PACKAGES}
   elif [ "${PKG_MANAGER}" = "brew" ]; then
      # brew refuses to run as root — use RunAsUser to drop to the original user
      RunAsUser brew install -q net-tools iproute2
   else
      # Fedora: iproute (not iproute2)
      REQUIRED_PACKAGES="python3-pip net-tools iproute"
      CheckCommand dnf install -q -y ${REQUIRED_PACKAGES}
   fi
}

InstallRequiredPipPackages()
{
   if [ "${PKG_MANAGER}" = "brew" ]; then
      # pip also must not run as root on Bazzite/brew systems
      RunAsUser pip install -q --ignore-installed --no-warn-script-location -r requirements.txt
   else
      CheckCommand pip install -q --break-system-packages --ignore-installed --no-warn-script-location -r requirements.txt
   fi
}

Main()
{
   echo "Running setup for spoofer"
   CheckForSudo
   DetectPackageManager
   if [ "${PKG_MANAGER}" = "brew" ]; then
      ResolveOriginalUser
   fi
   echo "-> Updating repos..."
   UpdateRepos
   echo "-> Installing system packages..."
   InstallRequiredPackages
   echo "-> Installing pip packages..."
   InstallRequiredPipPackages
   echo "Setup completed successfully!"
}

Main