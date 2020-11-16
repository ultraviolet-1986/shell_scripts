#!/usr/bin/env bash

###########
# License #
###########

# Shell Scripts: A collection of shell scripts in various languages.
# Copyright (C) 2020 William Willis Whinn

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

###############
# Description #
###############

# This script is intended to download, install, and configure the
# Anaconda 3 Python distribution without requiring user input. Current
# version: 2020.07.

#########
# Notes #
#########

# - The user's Terminal will require relaunching once the process is
#   complete.
# - This script assumes an active Internet connection is present.
# - This script must be executed as the current user, not root.

##############
# References #
##############

# Anaconda: Silent Installation
# - https://tinyurl.com/y6jfkcqn

# Verify SHA256SUM
# - https://tinyurl.com/yaue84sz

#############
# Variables #
#############

# Paths
readonly APPLICATION_FOLDER="$HOME/Downloads/Applications"
readonly ANACONDA_INSTALL_LOCATION="$HOME/anaconda3"

# Anaconda 3 Distribution (Linux x86_64)
readonly ANACONDA_URL='https://repo.anaconda.com/archive'
readonly ANACONDA_INSTALLER='Anaconda3-2020.07-Linux-x86_64.sh'
readonly ANACONDA_HASH='38ce717758b95b3bd0b1797cc6ccfb76f29a90c25bdfa50ee45f11e583edfdbf'

#############
# Functions #
#############

automate_anaconda3_installation() {
  # Create download directory (if not exists).
  mkdir -p "$APPLICATION_FOLDER"

  # Download the Anaconda installer to
  # "~/Downloads/Applications/<installer>".
  wget "$ANACONDA_URL/$ANACONDA_INSTALLER" -O "$APPLICATION_FOLDER/$ANACONDA_INSTALLER"

  # Check file hash using SHA-256.
  if (sha256sum -c <(echo "$ANACONDA_HASH $APPLICATION_FOLDER/$ANACONDA_INSTALLER")) ; then
    # SHA-256 checksum is valid, perform automatic installation.
    # NOTE: ASSUMES USER HAS AGREED TO EULA.
    bash "$APPLICATION_FOLDER/$ANACONDA_INSTALLER" -b -p "$ANACONDA_INSTALL_LOCATION" -f

    # Connect Anaconda to the user's shell (assume BASH).
    eval "$("$ANACONDA_INSTALL_LOCATION"/bin/conda shell.bash hook)"

    # Activate (base) on launch (default).
    "$ANACONDA_INSTALL_LOCATION"/bin/conda config --set auto_activate_base true

    # Initiate conda.
    "$ANACONDA_INSTALL_LOCATION"/bin/conda init
  else
    echo -e "Installer has not matched the SHA-256 checksum. Aborting."
    return
  fi

  echo -e "Anaconda has been installed on your system."
}

#############
# Kickstart #
#############

automate_anaconda3_installation

# End of File.
