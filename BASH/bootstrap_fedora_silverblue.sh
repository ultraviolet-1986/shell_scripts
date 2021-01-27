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

# This script is intended to help configure a fresh Fedora Silverblue
# installation. It will require a reboot between options and each option
# should be followed sequentially.

#############
# Variables #
#############

# Global Variables > Script Metadata

readonly SCRIPT_URL='https://github.com/ultraviolet-1986/shell_scripts'
readonly SCRIPT_VERSION='0.0.4'

# Global Variables > Text Formatting

readonly GREEN='\e[32m'
readonly RED='\e[31m'
readonly YELLOW='\e[33m'

readonly RESET='\e[0m'


#############
# Functions #
#############

# Functions > Prerequisites

test_network_connection() {
  if ( ping -c 1 1.1.1.1 ) &> /dev/null ; then
    return 0
  else
    return 1
  fi
}

# Functions > Main Menu

display_main_menu() {
  # Local Variables > Executable Paths
  local flatpak_path='/usr/bin/flatpak'
  local rpm_ostree_path='/usr/bin/rpm-ostree'

  # Failure: An active Internet connection was not detected.
  if ( ! test_network_connection ) ; then
    echo -e "\\n${RED}Error: An active Internet connection was not detected.${RESET}\\n"
    return 1

  # Failure: Flatpak package manager was not detected.
  elif [ ! -f "${flatpak_path}" ] ; then
    echo -e "\\n${RED}Error: Flatpak package manager was not detected.${RESET}\\n"
    return 1

  # Failure: RPM-OSTree package manager was not detected.
  elif [ ! -f "${rpm_ostree_path}" ] ; then
    echo -e "\\n${RED}Error: RPM-OSTree package manager was not detected.${RESET}\\n"
    return 1

  # Success: An active Internet connection was detected.
  # Success: Flatpak package manager was detected.
  # Success: RPM-OSTree package manager was detected.
  elif ( test_network_connection ) && [ -f "${flatpak_path}" ] && [ -f "${rpm_ostree_path}" ] ; then
    clear

    # Show Program Header.
    echo -e "Fedora Silverblue Bootstrap Script ${SCRIPT_VERSION}"
    echo "Copyright (C) 2020 William Whinn"
    echo -e "${SCRIPT_URL}\\n"

    # Show User Notice.
    echo -e "${YELLOW}Note: Perform each step sequentially and reboot after each.${RESET}\\n"

    # Show Main Menu Items.
    echo -e "  ${GREEN}1.${RESET} Update System Software"
    echo -e "  ${GREEN}2.${RESET} Install Software Repositories"
    echo -e "  ${GREEN}3.${RESET} Configure Preferred Software"
    echo -e "  ${GREEN}4.${RESET} Pin Current Deployment\\n"
    echo -e "  ${RED}X.${RESET} Exit Program\\n"

    # Take user input for selecting above options.
    printf "Please input your selection: "
    read -n1 -r answer
    echo

    case "$answer" in
      '1')
        update_system_software
        return 0
        ;;
      '2')
        install_software_repositories
        return 0
        ;;
      '3')
        configure_preferred_software
        return 0
        ;;
      '4')
        pin_current_deployment
        return 0
        ;;
      'X'|'x')
        echo
        return 0
        ;;
    esac

  # Failure: Catch All.
  else
    echo -e "\\n${RED}Error: An unknown error occurred.${RESET}\\n"
    return 1
  fi
}

# Functions > Main Menu > Option 1

update_system_software() {
  clear

  # Update RPM software.
  echo -e "${YELLOW}Note: Updating RPM System Software.${RESET}\\n"
  rpm-ostree refresh-md &&
  rpm-ostree upgrade

  # Remove unused Flatpak software.
  flatpak uninstall -y org.gnome.Calendar
  flatpak uninstall -y org.gnome.Contacts
  flatpak uninstall -y org.gnome.Maps
  flatpak uninstall -y org.gnome.Weather

  flatpak uninstall --unused

  # Update Flatpak softare.
  echo -e "${YELLOW}Note: Updating Flatpak System Software.${RESET}\\n"
  flatpak update

  echo -e "\\n${GREEN}Success: Please Reboot and select Option 2.${RESET}\\n"
  return 0
}

# Functions > Main Menu > Option 2

install_software_repositories() {
  # Local Variables > Repository File Paths
  local chrome_repo_file='/etc/yum.repos.d/google-chrome.repo'
  local code_repo_file='/etc/yum.repos.d/vscode.repo'
  # local skype_repo_file='/etc/yum.repos.d/skype-stable.repo'
  local teams_repo_file='/etc/yum.repos.d/teams.repo'

  # Local Variables > Get Fedora Version
  local rel
  rel="$(rpm -E %fedora)"

  clear
  echo -e "${YELLOW}Note: Installing Software Repositories.${RESET}\\n"

  # Google Chrome Repository
  echo -e "${YELLOW}Installing Google Chrome Repository.${RESET}"

  echo '[google-chrome]' | sudo tee "$chrome_repo_file" &&
  echo 'name=google-chrome' | sudo tee -a "$chrome_repo_file" &&
  echo 'baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64' | \
    sudo tee -a "$chrome_repo_file" &&
  echo 'enabled=1' | sudo tee -a "$chrome_repo_file" &&
  echo 'gpgcheck=1' | sudo tee -a "$chrome_repo_file" &&
  echo 'gpgkey=https://dl.google.com/linux/linux_signing_key.pub' | sudo tee -a "$chrome_repo_file"
  echo

  # # Skype Repository
  # echo -e "${YELLOW}Installing Skype Repository.${RESET}"

  # echo '[skype-stable]' | sudo tee "$skype_repo_file" &&
  # echo 'name=skype (stable)' | sudo tee -a "$skype_repo_file" &&
  # echo 'baseurl=https://repo.skype.com/rpm/stable' | sudo tee -a "$skype_repo_file" &&
  # echo 'enabled=1' | sudo tee -a "$skype_repo_file" &&
  # echo 'gpgcheck=1' | sudo tee -a "$skype_repo_file" &&
  # echo 'gpgkey=https://repo.skype.com/data/SKYPE-GPG-KEY' | sudo tee -a "$skype_repo_file"
  # echo

  # Teams Repository
  echo -e "${YELLOW}Installing Microsoft Teams Repository.${RESET}"

  echo '[teams]' | sudo tee "$teams_repo_file" &&
  echo 'name=teams' | sudo tee -a "$teams_repo_file" &&
  echo 'baseurl=https://packages.microsoft.com/yumrepos/ms-teams' | \
    sudo tee -a "$teams_repo_file" &&
  echo 'enabled=1' | sudo tee -a "$teams_repo_file" &&
  echo 'gpgcheck=1' | sudo tee -a "$teams_repo_file" &&
  echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' | \
    sudo tee -a "$teams_repo_file" &&
  echo

  # Visual Studio Code Repository
  echo -e "${YELLOW}Installing Visual Studio Code Repository.${RESET}"

  echo '[code]' | sudo tee "$code_repo_file" &&
  echo 'name=Visual Studio Code' | sudo tee -a "$code_repo_file" &&
  echo 'baseurl=https://packages.microsoft.com/yumrepos/vscode' | sudo tee -a "$code_repo_file" &&
  echo 'enabled=1' | sudo tee -a "$code_repo_file" &&
  echo 'gpgcheck=1' | sudo tee -a "$code_repo_file" &&
  echo 'gpgkey=https://packages.microsoft.com/keys/microsoft.asc' | sudo tee -a "$code_repo_file"
  echo

  # RPMFusion Repository
  echo -e "${YELLOW}Installing RPMFusion Repository.${RESET}"

  rpm-ostree install \
    "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-${rel}.noarch.rpm" \
    "https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-${rel}.noarch.rpm"
  echo

  # Update Flatpak software and install Flathub repository.
  echo -e "${YELLOW}Note: Installing Flathub remote for Flatpak${RESET}\\n"
  flatpak remote-add --if-not-exists flathub "https://flathub.org/repo/flathub.flatpakrepo"

  # Prompt user for reboot before continuing.
  echo -e "\\n${GREEN}Success: Please Reboot and select Option 3.${RESET}\\n"
  return 0
}

# Functions > Main Menu > Option 3

configure_preferred_software() {
  clear

  # Install Flatpak Software.
  echo -e "${YELLOW}Note: Installing preferred Flatpak software from Flathub Remote.${RESET}\\n"
  flatpak install flathub -y "com.transmissionbt.Transmission"
  flatpak install flathub -y "org.gimp.GIMP"
  flatpak install flathub -y "org.gnome.Boxes"
  flatpak install flathub -y "org.libreoffice.LibreOffice"
  echo

  # Install RPM Software.
  echo -e "${YELLOW}Note: Installing RPM software from sources configured in Option 2.${RESET}\\n"
  rpm-ostree install \
    clamav \
    clamav-update \
    code \
    evolution \
    exfat-utils \
    ffmpeg \
    fuse-exfat \
    gcc \
    'gcc-c++' \
    genisoimage \
    gnome-tweaks \
    google-chrome-stable \
    java-11-openjdk-headless \
    joystick-support \
    mpv \
    simple-scan \
    squashfs-tools \
    teams \
    vim \
    youtube-dl \
    'https://us02web.zoom.us/client/latest/zoom_x86_64.rpm' # Install Zoom.

  echo -e "\\n${GREEN}Success: Please Reboot and select Option 4.${RESET}\\n"
  return 0
}

# Functions > Main Menu > Option 4

pin_current_deployment() {
  clear

  echo -e "${YELLOW}Note: Pinning Current Deployment${RESET}\\n"
  sudo ostree admin pin 0

  echo -e "\\n${GREEN}Success: Process Complete.${RESET}\\n"
  return 0
}

#############
# Kickstart #
#############

display_main_menu

# End of File.
