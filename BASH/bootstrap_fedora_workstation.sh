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

###############
# Description #
###############

# This script is intended to bootstrap a new Fedora Workstation system
# autonomously without requiring user-input.

#########
# Notes #
#########

# - It is considered bad practise to include 'sudo' commands within a
#   script.
# - Script may be run with `sudo bash fedora_bootstrap_sudo.sh`.
# - Please read and configure this script before executing.
# - Please ensure you understand what this script is doing before
#   execution.
# - This script is intended to be ran only once after installation has
#   been completed.
# - The system will require a reboot once the bootstrapping process has
#   completed.
# - This script assumes an active Internet connection is present.

#############
# Functions #
#############

# DNF SOFTWARE CONFIGURATION

remove_unused_software() {
  sudo dnf remove -y \
    cheese \
    gnome-calendar \
    gnome-contacts \
    gnome-documents \
    gnome-maps \
    gnome-photos \
    gnome-weather \
    rhythmbox \
    totem

  echo
  return 0
}

perform_system_update() {
  sudo dnf update --refresh -y

  echo
  return 0
}

# DNF REPOSITORY SOFTWARE

install_repository_rpmfusion() {
  local rel="$(rpm -E %fedora)"

  sudo dnf install -y \
    "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-${rel}.noarch.rpm" \
    "https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-${rel}.noarch.rpm"

  # Update software groups for software manager.
  sudo dnf groupupdate -y core
  sudo dnf groupupdate -y multimedia
  sudo dnf groupupdate -y sound-and-video

  echo
  return 0
}

install_visual_studio_code() {
  # Import repository key.
  sudo rpm --import 'https://packages.microsoft.com/keys/microsoft.asc'

  local code_repo_file='/etc/yum.repos.d/vscode.repo'

  echo '[code]' | sudo tee "$code_repo_file" &&
  echo 'name=Visual Studio Code' | sudo tee -a "$code_repo_file" &&
  echo 'baseurl=https://packages.microsoft.com/yumrepos/vscode' | sudo tee -a "$code_repo_file" &&
  echo 'enabled=1' | sudo tee -a "$code_repo_file" &&
  echo 'gpgcheck=1' | sudo tee -a "$code_repo_file" &&
  echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' | sudo tee -a "$code_repo_file"

  echo
  sudo dnf install -y code

  echo
  return 0
}

install_microsoft_fonts() {
  local url='https://downloads.sourceforge.net/project/mscorefonts2/rpms'
  local filename='msttcore-fonts-installer-2.6-1.noarch.rpm'
  sudo dnf install -y "${url}/${filename}"

  echo
  return 0
}

install_skype() {
  sudo dnf install -y 'https://repo.skype.com/latest/skypeforlinux-64.rpm'

  echo
  return 0
}

install_google_chrome() {
  sudo dnf install -y 'https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm'

  echo
  return 0
}

install_preferred_software() {
  sudo dnf install -y \
    clamav \
    clamav-update \
    evolution \
    exfat-utils \
    ffmpeg \
    fuse-exfat \
    genisoimage \
    git \
    gnome-terminal-nautilus \
    gnome-tweaks \
    joystick-support \
    kernel-modules-extra \
    mesa-libGLU \
    mpv \
    nano \
    p7zip \
    spice-vdagent \
    spice-webdavd \
    timeshift \
    transmission \
    vlgothic-fonts \
    vlgothic-p-fonts

  echo
  return 0
}

# DNF DEVELOPMENT

install_rstudio() {
  # Install R and RStudio with dependencies for building packages.
  sudo dnf install -y \
    compat-openssl10 \
    libcurl-devel \
    libjpeg-turbo-devel \
    libsodium-devel \
    libxml2-devel \
    openssl-devel \
    R \
    R-Rcpp \
    R-Rcpp-devel \
    rstudio-desktop \
    udunits2-devel

  # Remove unused Java menu entries (system-wide).
  for f in /usr/share/applications/java-1.8.0-openjdk-1.8.0*.desktop ; do
    echo -e "NoDisplay=true" | sudo tee --append "$f" > /dev/null
  done

  echo
  return 0
}

install_ruby() {
  sudo dnf install -y \
    ruby \
    ruby-devel \
    rubygem-bundler \
    rubygem-rake

  echo
  return 0
}

# DNF VIRTUALISATION SOFTWARE

install_oracle_virtualbox() {
  sudo wget \
    "https://download.virtualbox.org/virtualbox/rpm/fedora/virtualbox.repo" -O \
    "/etc/yum.repos.d/virtualbox.repo"

  sudo dnf install -y VirtualBox-6.1

  sudo usermod -aG vboxusers "$USER"

  echo
  return 0
}

# DNF DRIVER SOFTWARE

install_intel_drivers() {
  sudo dnf install -y \
    intel-gpu-tools \
    libva-intel-driver \
    xorg-x11-drv-intel

  echo
  return 0
}

# UNIVERSAL SOFTWARE CONFIGURATION

# FLATPAK

configure_flathub() {
  flatpak remote-add --if-not-exists flathub 'https://flathub.org/repo/flathub.flatpakrepo'

  echo
  return 0
}

# SNAP

configure_snapd() {
  sudo dnf install -y snapd

  # Create symlink to allow classic-confinement applications.
  sudo ln -s '/var/lib/snapd/snap' '/snap'

  # Enable 'snapd' service and start immediately.
  sudo systemctl enable snapd
  sudo systemctl start snapd

  echo
  return 0
}

# UPDATE CLAMAV

update_clamav_database() {
  sudo freshclam

  echo
  return 0
}

#############
# Kickstart #
#############

# DNF SOFTWARE CONFIGURATION

remove_unused_software
perform_system_update

# DNF REPOSITORY SOFTWARE

install_repository_rpmfusion
install_visual_studio_code
install_microsoft_fonts
install_skype
# install_google_chrome

install_preferred_software

# DNF DEVELOPMENT SOFTWARE

# install_rstudio
# install_ruby

# DNF VIRTUALISATION SOFTWARE

# install_oracle_virtualbox

# DNF DRIVER SOFTWARE

install_intel_drivers # Comment for AMD-based systems.

# UNIVERSAL SOFTWARE CONFIGURATION

# FLATPAK
configure_flathub

# SNAP
configure_snapd

# UPDATE CLAMAV

update_clamav_database

# End of File.
