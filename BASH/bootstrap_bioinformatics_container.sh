#!/usr/bin/env bash

###########
# License #
###########

# Shell Scripts: A collection of shell scripts in various languages.
# Copyright (C) 2021 William Willis Whinn

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
# Version: 0.1.2
# Date:    26th February 2021

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
# - WINE and Winetricks are included to help run software designed for
#   the Microsoft Windows platform.

#############
# Resources #
#############

# - MEGAX
#   https://tinyurl.com/595fhpuw

# - Microsoft Core Fonts
#   https://tinyurl.com/tt6ay23t

# - MODELLER
#   https://salilab.org/modeller/

# - NCBI BLAST Software and Documentation
#   https://tinyurl.com/y9nf9q2g

# - NCBI BLAST+ Documentation
#   https://tinyurl.com/ya3rnwpc

# - NCBI BLAST Database Documentation
#   https://tinyurl.com/y73gbneq

# - NCBI BLAST Databases
#   https://ftp.ncbi.nlm.nih.gov/blast/db/

# - Pajek
#   http://mrvar.fdv.uni-lj.si/pajek/

# - SnapGene Viewer
#   https://tinyurl.com/9tmbehx8

# - VESTA
#   http://jp-minerals.org/vesta/en/

############
# Commands #
############

# The included applications are listed below. Note that some software
# comes from third party websites outside of the official Fedora
# software repositories. Because of this, the user is advised to
# continue at their own discretion.

# | Software Name   | Command         |
# |-----------------|-----------------|
# | BLASTn          | blastn          |
# | BLASTp          | blastp          |
# | BLASTx          | blastx          |
# | COPASI          | CopasiUI        |
# | DeltaBLAST      | deltablast      |
# | MegaX           | mega            |
# | MODELLER        | mod10.0         |
# | pandoc          | pandoc          |
# | PSI-BLAST       | psiblast        |
# | PyMOL           | pymol           |
# | R               | R               |
# | rpBLAST         | rpblast         |
# | rpstBLASTn      | rpstblastn      |
# | RStudio         | rstudio         |
# | SnapGene Viewer | snapgene-viewer |
# | tBLASTn         | tblastn         |
# | tBLASTx         | tblastx         |
# | VESTA           | VESTA           |
# | WINE            | wine            |
# | Winetricks      | winetricks      |

#############
# Variables #
#############

# NOTE Assumes site(s) and RPM are secure. Use at your own discretion.

# NCBI BLAST+
readonly BLAST_URL='https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.11.0'
readonly BLAST_RPM="${BLAST_URL}/ncbi-blast-2.11.0+-1.x86_64.rpm"

# NCBI Magic-BLAST
readonly MAGIC_URL='https://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/1.6.0'
readonly MAGIC_RPM="${MAGIC_URL}/ncbi-magicblast-1.6.0-1.x86_64.rpm"

# NCBI IgBLAST
readonly IG_URL='https://ftp.ncbi.nih.gov/blast/executables/igblast/release/1.17.1'
readonly IG_RPM="${IG_URL}/ncbi-igblast-1.17.1-1.x86_64.rpm"

# Microsoft Core Fonts
readonly FONT_URL='https://downloads.sourceforge.net/project/mscorefonts2/rpms'
readonly FONT_RPM="${FONT_URL}/msttcore-fonts-installer-2.6-1.noarch.rpm"

# MEGAX
readonly MEGAX_URL='https://www.megasoftware.net/releases'
readonly MEGAX_RPM="${MEGAX_URL}/megax-10.2.5-1.x86_64.rpm"

# MODELLER
readonly MODELLER_URL='https://salilab.org/modeller/10.1'
readonly MODELLER_RPM="${MODELLER_URL}/modeller-10.1-1.x86_64.rpm"

# SNAPGENE VIEWER
readonly SNAPGENE_URL='https://cdn.snapgene.com/downloads/SnapGeneViewer/5.x/5.2/5.2.5'
readonly SNAPGENE_RPM="${SNAPGENE_URL}/snapgene_viewer_5.2.5_linux.rpm"

# VESTA
readonly VESTA_URL='http://jp-minerals.org/vesta/archives/3.5.7'
readonly VESTA_RPM="${VESTA_URL}/vesta-3.5.7-1.x86_64.rpm"

#############
# Functions #
#############

bootstrap_bioinformatics_container() {
  # ShellCheck Directives
  # <https://github.com/koalaman/shellcheck/wiki/SC2035>
  # shellcheck disable=SC2035

  # ShellCheck Notes
  # - Package selection '*adwaita*' is intended to install all packages
  #   associated to that theme, including Qt5 versions.

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
      *adwaita* \
      adobe-source-code-pro-fonts \
      byobu \
      cairo-devel \
      COPASI \
      COPASI-gui \
      fira-code-fonts \
      gnu-free-mono-fonts \
      ibm-plex-mono-fonts \
      julia \
      julia-common \
      julia-devel \
      julia-doc \
      libcanberra* \
      libcurl-devel \
      liberation-fonts \
      liberation-mono-fonts \
      libgfortran \
      libgit2-devel \
      libjpeg-turbo-devel \
      libsodium-devel \
      libxml2-devel \
      mozilla-fira-mono-fonts \
      nano \
      openssl-devel \
      pandoc \
      perl-CPAN \
      pymol \
      python3-COPASI \
      python3-tkinter \
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
      wine \
      winetricks \
      zenity \
      "${BLAST_RPM}" \
      "${MAGIC_RPM}" \
      "${IG_RPM}" \
      "${FONT_RPM}" \
      "${MEGAX_RPM}" \
      "${MODELLER_RPM}" \
      "${SNAPGENE_RPM}" \
      "${VESTA_RPM}"

    # Install the PERL JSON module for use with BLAST.
    toolbox run --container bioinformatics 'sudo' 'cpan' 'JSON'

    echo -e "\nPlease insert your MODELLER key the file:"
    echo -e "'/usr/lib/modeller10.0/modlib/modeller/config.py'\n"

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
