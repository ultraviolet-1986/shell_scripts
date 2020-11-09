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
# along with this program. If not, see <http:#www.gnu.org/licenses/>.

#########
# Notes #
#########

# - This script assumes a Fedora Workstation or Fedora Silverblue host
#   machine.
# - This script requires Fedora Toolbox to be installed and an active
#   Internet connection.
# - This script pings the CloudFlare DNS to check for an active Internet
#   connection.
# - Additional packages are installed which are for building R packages
#   from source.
# - RStudio can be started within this container by using the `rstudio`
#   command.

#############
# Functions #
#############

bootstrap_r_development_container()
{
  local centos_mirror='http://mirror.centos.org/centos/7/os/x86_64/Packages'

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
      'adwaita-qt' \
      'adwaita-qt4' \
      'adwaita-qt5' \
      'adwaita-qt-common' \
      'cairo-devel' \
      'compat-openssl10' \
      'libcanberra-gtk3' \
      'libcurl-devel' \
      'liberation-fonts' \
      'libgfortran' \
      'libjpeg-turbo-devel' \
      'libsodium-devel' \
      'libxml2-devel' \
      'openssl-devel' \
      'qgnomeplatform' \
      'qt5-qtbase' \
      'qt5-qtbase-common' \
      'qt5-qtbase-gui' \
      'qt5-qtdeclarative' \
      'qt5-qtwayland' \
      'qt5-qtx11extras' \
      'qt5-qtxmlpatterns' \
      'R' \
      'R-Rcpp' \
      'R-Rcpp-devel' \
      'rstudio-desktop' \
      'udunits2-devel' \
      "$centos_mirror/libgfortran4-8.3.1-2.1.1.el7.x86_64.rpm" # Fedora Compatible.

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

bootstrap_r_development_container

# End of File.
