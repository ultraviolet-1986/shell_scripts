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

#########
# Notes #
#########

# - This script assumes a Fedora Workstation or Fedora Silverblue host
#   machine.
# - This script requires Fedora Toolbox to be installed and an active
#   Internet connection.
# - This script pings the CloudFlare DNS to check for an active
#   Internet connection.
# - RStudio can be started within this container by using the `rstudio`
#   command.
# - If you are using the Anaconda Python distribution, please use the
#   command `conda deactivate` when entering the container as this WILL
#   cause problems with building R packages from source. This container
#   should have all of the neccesary libraries installed by default.

#############
# Functions #
#############

bootstrap_rstudio_container()
{
  if ( command -v 'toolbox' > /dev/null 2>&1 ) && ( ping -c 1 1.1.1.1 ) &> /dev/null ; then
    # Create a Fedora Toolbox named 'rdev'.
    toolbox create --container rdev

    # Update the new 'rdev' toolbox.
    toolbox run --container rdev 'sudo' 'dnf' 'update' '--refresh' '-y'

    # Install R development software into the 'rdev' container.
    toolbox run --container rdev 'sudo' 'dnf' 'install' '-y' \
      'adobe-source-code-pro-fonts' \
      'adwaita-gtk2-theme' \
      'adwaita-icon-theme' \
      'adwaita-qt-common' \
      'adwaita-qt' \
      'adwaita-qt4' \
      'adwaita-qt5' \
      'cairo-devel' \
      'compat-openssl10' \
      'fira-code-fonts' \
      'gnu-free-mono-fonts' \
      'ibm-plex-mono-fonts' \
      'libcanberra-gtk3' \
      'libcurl-devel' \
      'liberation-fonts' \
      'liberation-mono-fonts' \
      'libgfortran' \
      'libgit2-devel' \
      'libjpeg-turbo-devel' \
      'libsodium-devel' \
      'libxml2-devel' \
      'mozilla-fira-mono-fonts' \
      'openssl-devel' \
      'qgnomeplatform' \
      'qt5-qtbase-common' \
      'qt5-qtbase-gui' \
      'qt5-qtbase' \
      'qt5-qtdeclarative' \
      'qt5-qtwayland' \
      'qt5-qtx11extras' \
      'qt5-qtxmlpatterns' \
      'R-Rcpp-devel' \
      'R-Rcpp' \
      'R' \
      'rstudio-desktop' \
      'texlive-inconsolata' \
      'texlive-typewriter' \
      'udunits2-devel'

    # Stop and exit the container if Toolbox has not stopped it.
    sleep 1
    podman stop rdev

    return 0

  elif ( ! command -v 'toolbox' > /dev/null 2>&1 ) ; then
    echo -e "ERROR: This program requires package 'toolbox' to be installed."
    return 127

  elif ( ! ping -c 1 1.1.1.1 ) &> /dev/null ; then
    echo -e "ERROR: This program requires an active Internet connection."
    return 1

  else
    echo -e "ERROR: An unknown error occurred."
    return 1
  fi
}

#############
# Kickstart #
#############

bootstrap_rstudio_container

# End of File.
