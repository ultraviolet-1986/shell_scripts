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

# Author............: William Whinn
# Script name.......: bootstrap_ubuntu_workstation.sh
# Script created....: 13th October 2021
# Script updated....: 13th October 2021
# Script version....: 0.0.1
# Script URL........: https://github.com/ultraviolet-1986/shell_scripts

#########
# Notes #
#########

# - This script assumes a vanilla Ubuntu minimal installation.
# - Snap software is preferred for third-party applications.
# - DEB software is preferred for system libraries or desktop
#   utilities.
# - This script will download scripts, wallpapers, and software from
#   the Internet. Execute this script ONLY if you trust the code.

#############
# Functions #
#############

# FUNCTIONS > CONFIGURATION

create_mpv_config(){
  mkdir -p "$HOME/.config/mpv"

  {
    echo "load-unsafe-playlists"
    echo "loop-playlist"
    echo "# shuffle"
    echo "sub-auto=all"
    echo "window-scale=0.70"
  } > "$HOME/.config/mpv/mpv.conf"

  echo
  return 0
}

# FUNCTIONS > APPEARANCE

configure_default_wallpaper(){
  local wallpaper_file="ytkkbowirm061.jpg"
  local wallpaper_url="https://i.redd.it/$wallpaper_file"
  local wallpaper_dir="$HOME/Pictures/Wallpapers"

  mkdir -p "$wallpaper_dir"
  cd "$wallpaper_dir" || return 1
  wget "$wallpaper_url"
  cd ~- || return 1

  gsettings set org.gnome.desktop.background picture-uri "file://$wallpaper_dir/$wallpaper_file"

  echo
  return 0
}

disable_desktop_icons(){
  gnome-extensions disable desktop-icons@csoriano
}

configure_gnome_dock(){
  gsettings set org.gnome.shell.extensions.dash-to-dock dock-fixed false
  gsettings set org.gnome.shell.extensions.dash-to-dock autohide true
  gsettings set org.gnome.shell.extensions.dash-to-dock intellihide true
  gsettings set org.gnome.shell.extensions.dash-to-dock intellihide-mode \
    'FOCUS_APPLICATION_WINDOWS'
  gsettings set org.gnome.shell.extensions.dash-to-dock click-action \
    'minimize'
}

sort_menu_items(){
  local script_file="appfixer.sh"
  local script_url="https://raw.githubusercontent.com/BenJetson/gnome-dash-fix/master/$script_file"
  local workspace_dir="$HOME/Documents/Workspace/BASH"
  
  mkdir -p "$workspace_dir"
  cd "$workspace_dir" || return 1
  wget "$script_url"
  cd ~- || return 1

  bash "$workspace_dir/$script_file"

  echo
  return 0
}

# FUNCTIONS > SECURITY

configure_ufw_filewall(){
  sudo ufw enable
  sudo ufw default deny
  sudo ufw limit ssh

  echo
  return 0
}

# FUNCTIONS > SOFTWARE

remove_unused_software(){
  sudo apt remove -y \
    firefox \
    rhythmbox \
    totem

  sudo apt clean
  sudo apt autoremove -y

  echo
  return 0
}

update_apt_software(){
  sudo apt update && \
  sudo apt full-upgrade -y || return 1

  echo
  return 0
}

update_snap_software(){
  sudo snap refresh
  echo
  return 0
}

install_preferred_apt_software(){
  sudo apt install -y \
    build-essential \
    clamav \
    curl \
    dkms \
    evolution \
    genisoimage \
    git \
    gnome-disk-utility \
    gnome-shell-extension-prefs \
    gnome-tweaks \
    "linux-headers-$(uname -r)" \
    mpv \
    nano \
    p7zip-full \
    squashfs-tools \
    timeshift \
    tree \
    ubuntu-restricted-extras \
    unrar

  echo
  return 0
}

install_google_chrome(){
  local deb_file="google-chrome-stable_current_amd64.deb"
  local deb_url="https://dl.google.com/linux/direct/$deb_file"
  local download_dir="$HOME/Downloads/Applications"

  mkdir -p "$download_dir"
  cd "$download_dir" || return 1
  wget "$deb_url"
  sudo apt install -y ./"$deb_file"
  cd ~- || return 1

  echo
  return 0
}

install_preferred_snap_software(){
  sudo snap install code --classic
  sudo snap install firefox
  sudo snap install gimp
  sudo snap install libreoffice
  sudo snap install teams

  echo
  return 0
}

#############
# Kickstart #
#############

# FUNCTIONS > SECURITY
configure_ufw_filewall

# FUNCTIONS > CONFIGURATION
create_mpv_config

# FUNCTIONS > APPEARANCE
configure_default_wallpaper
disable_desktop_icons
configure_gnome_dock
sort_menu_items

# FUNCTIONS > SOFTWARE
remove_unused_software
update_apt_software
update_snap_software
install_preferred_apt_software
install_google_chrome
install_preferred_snap_software

# End of File.

