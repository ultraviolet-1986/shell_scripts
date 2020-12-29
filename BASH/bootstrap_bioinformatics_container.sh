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

############
# Metadata #
############

# Author:  William Whinn
# Version: 0.0.1
# Date:    27th December 2020

#########
# Notes #
#########

# - This script assumes a Fedora Workstation or Fedora Silverblue host
#   machine.
# - This script requires Fedora Toolbox to be installed and an active
#   Internet connection.
# - This script pings the CloudFlare DNS to check for an active
#   Internet connection.
# - If you are using the Anaconda Python distribution, please use the
#   command `conda deactivate` when entering the container as this WILL
#   cause problems with building R packages from source. This container
#   should have all of the neccesary libraries installed by default.
# - In academic work, the user may be required to cite the applications
#   used and are expected to do so in accordance with the terms of the
#   software package(s) license.

############
# Commands #
############

# The included applications are listed below. Note that some software
# comes from third party websites outside of the official Fedora
# software repositories. Because of this, the user is advised to
# continue at their own discretion.

# | Software Name | Command |
# |---------------|---------|
# | MegaX         | mega    |
# | PyMOL         | pymol   |
# | R             | R       |
# | RStudio       | rstudio |

#############
# Variables #
#############

# NOTE Assumes site(s) and RPM are secure. Use at your own discretion.

readonly FONT_URL='https://downloads.sourceforge.net/project/mscorefonts2/rpms'
readonly FONT_RPM="${FONT_URL}/msttcore-fonts-installer-2.6-1.noarch.rpm"

readonly MEGAX_URL='https://www.megasoftware.net/do_force_download'
readonly MEGAX_RPM="${MEGAX_URL}/megax-10.2.2-1.x86_64.rpm"

#############
# Functions #
#############

bootstrap_bioinformatics_container() {
  if ( command -v 'toolbox' > /dev/null 2>&1 ) && \
    ( ping -c 1 1.1.1.1 ) &> /dev/null ; then

    # Create a Fedora Toolbox named 'bioinformatics'.
    toolbox create --container bioinformatics

    # Update the new 'bioinformatics' toolbox.
    toolbox run --container bioinformatics \
      'sudo' 'dnf' 'update' '--refresh' '-y'

    # Install software and dependencies into the 'bioinformatics'
    # container.
    toolbox run --container bioinformatics 'sudo' 'dnf' 'install' '-y' \
      adobe-source-code-pro-fonts \
      adwaita-gtk2-theme \
      adwaita-icon-theme \
      adwaita-qt \
      adwaita-qt* \
      adwaita-qt4 \
      adwaita-qt5 \
      adwaita-qt-common \
      adwaita*theme* \
      cairo-devel \
      compat-openssl10 \
      fira-code-fonts \
      gnu-free-mono-fonts \
      ibm-plex-mono-fonts \
      libcanberra-gtk3 \
      libcurl-devel \
      liberation-fonts \
      liberation-mono-fonts \
      libgfortran \
      libgit2-devel \
      libjpeg-turbo-devel \
      libsodium-devel \
      libxml2-devel \
      mozilla-fira-mono-fonts \
      openssl-devel \
      pymol \
      qgnomeplatform \
      qt5-qtbase \
      qt5-qtbase-common \
      qt5-qtbase-gui \
      qt5-qtdeclarative \
      qt5-qtwayland \
      qt5-qtx11extras \
      qt5-qtxmlpatterns \
      R \
      R-Rcpp \
      R-Rcpp-devel \
      rstudio-desktop \
      texlive-inconsolata \
      texlive-typewriter \
      udunits2-devel \
      "$FONT_RPM" \
      "$MEGAX_RPM"

    # Stop and exit the container if Toolbox has not stopped it.
    sleep 1
    podman stop bioinformatics

    return 0

  elif ( ! command -v 'toolbox' > /dev/null 2>&1 ) ; then
    echo "ERROR: This program requires package 'toolbox' to be installed."
    return 127

  elif ( ! ping -c 1 1.1.1.1 ) &> /dev/null ; then
    echo "ERROR: This program requires an active Internet connection."
    return 1

  else
    echo "ERROR: An unknown error occurred."
    return 1
  fi
}

#############
# Kickstart #
#############

bootstrap_bioinformatics_container

# End of File.
