#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manage and maintain your Linux installation."""

##############
# References #
##############

# Detect Internet Connection ..................... https://tinyurl.com/yc44q3b4

###########
# Imports #
###########

import os
import socket
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata
SCRIPT_VERSION = '0.1.4'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell_scripts'

# String colours and formatting
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
MAGENTA = '\033[0;35m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'

LIGHT_BLUE = '\033[0;94m'
LIGHT_CYAN = '\033[0;96m'
LIGHT_GREEN = '\033[0;92m'
LIGHT_MAGENTA = '\033[0;95m'
LIGHT_RED = '\033[0;91m'
LIGHT_YELLOW = '\033[0;93m'

BLACK = '\033[0;30m'
GREY = '\033[0;90m'
WHITE = '\033[0;97m'

BOLD = '\033[1m'
UNDERLINE = '\033[4m'

COLOUR_RESET = '\033[0;m'

# Environmental Variables
HOME = os.environ['HOME']

# System Package Manager executables
APT = '/usr/bin/apt'
DNF = '/usr/bin/dnf'
RPM_OSTREE = '/usr/bin/rpm-ostree'

# Universal Package Manager executables
FLATPAK = '/usr/bin/flatpak'
SNAP = '/usr/bin/snap'

# Anaconda (User-Installed) Package Manager executables
ANACONDA = "{0}/anaconda3/bin/anaconda".format(HOME)
CONDA = "{0}/anaconda3/bin/conda".format(HOME)

# ClamAV Executables
FRESHCLAM = '/usr/bin/freshclam'

#############
# Functions #
#############

def clear():
    """Clear the current Terminal window."""
    os.system('clear')


def check_network_connection():
    """Detect whether or not an active Internet connection is available."""
    try:
        socket.create_connection(('1.1.1.1', 80))
        return True
    except OSError:
        return False


def linux_setup_menu():
    """Clear the screen and display the main menu."""

    clear()

    print('{0}Linux System Maintenance Utility {1}{2}'.format(BOLD,
                                                              SCRIPT_VERSION,
                                                              COLOUR_RESET))
    print('Copyright (C) 2020 William Whinn')
    print("{0}\n".format(SCRIPT_URL))

    # Display Main Menu
    print('  {0}1.{1} Update System Software'.format(LIGHT_GREEN,
                                                     COLOUR_RESET))
    print('  {0}2.{1} Update ClamAV Virus Definitions'.format(LIGHT_GREEN,
                                                              COLOUR_RESET))
    print()
    print('  {0}X.{1} Exit Program\n'.format(LIGHT_RED, COLOUR_RESET))

    answer = input("Please enter your selection: ")

    if answer == '1':
        clear()
        update_system_software()
    elif answer == '2':
        clear()
        update_clamav_definitions()
    elif answer in ('X', 'x'):
        clear()
        sys.exit()
    else:
        print()
        sys.exit('ERROR: Incorrect response\n')


def update_system_software():
    """Detect various package managers and update system software."""

    # Native Package Managers: DNF, APT, etc.
    if os.path.exists(APT):
        print("{0}APT System Software Section{1}".format(LIGHT_YELLOW,
                                                         COLOUR_RESET))
        subprocess.run('sudo {0} update'.format(APT),
                       shell=True, check=True)
        print()
        subprocess.run('sudo {0} full-upgrade'.format(APT),
                       shell=True, check=True)
        print()

    elif os.path.exists(DNF):
        print("{0}DNF System Software Section{1}".format(LIGHT_YELLOW,
                                                         COLOUR_RESET))
        subprocess.run('sudo {0} update --refresh'.format(DNF),
                       shell=True, check=True)
        print()

    elif os.path.exists(RPM_OSTREE):
        print("{0}RPM-OSTree System Software Section{1}".format(LIGHT_YELLOW,
                                                                COLOUR_RESET))
        subprocess.run('{0} refresh-md'.format(RPM_OSTREE),
                       shell=True, check=True)
        print()
        subprocess.run('{0} upgrade'.format(RPM_OSTREE),
                       shell=True, check=True)
        print()

    else:
        sys.exit("{0}Could not detect a native package manager. Exiting.{1}\n"
                 .format(LIGHT_RED, COLOUR_RESET))

    # Universal Package Managers: Flatpak, Snap, etc.
    if os.path.exists(FLATPAK):
        print("{0}Flatpak Universal Software Section{1}".format(LIGHT_YELLOW,
                                                                COLOUR_RESET))
        subprocess.run('{0} update'.format(FLATPAK),
                       shell=True, check=True)
        print()
    else:
        pass

    if os.path.exists(SNAP):
        print("{0}Snap Universal Software Section{1}".format(LIGHT_YELLOW,
                                                             COLOUR_RESET))
        subprocess.run('{0} refresh'.format(SNAP),
                       shell=True, check=True)
        print()
    else:
        pass

    if os.path.exists(CONDA):
        print("{0}Anaconda 3 Python Distribution Section{1}".format
              (LIGHT_YELLOW,
               COLOUR_RESET))
        subprocess.run('{0} update conda'.format(CONDA),
                       shell=True, check=True)
        subprocess.run('{0} update anaconda'.format(CONDA),
                       shell=True, check=True)
    else:
        pass

    sys.exit("{0}System software has been updated.{1}\n".format(LIGHT_GREEN,
                                                                COLOUR_RESET))


def update_clamav_definitions():
    """Update Antivirus definitions for ClamAV (if installed)."""

    if os.path.exists(FRESHCLAM):
        print("{0}ClamAV Antivirus Definitions Update{1}".format(LIGHT_YELLOW,
                                                                 COLOUR_RESET))
        subprocess.run('sudo {0}'.format(FRESHCLAM), shell=True, check=True)
        print()

        sys.exit("{0}ClamAV virus definitions have been updated.{1}\n"
                 .format(LIGHT_GREEN, COLOUR_RESET))
    elif not os.path.exists(FRESHCLAM):
        sys.exit("\n{0}ClamAV 'freshclam' is not installed. Exiting.{1}\n"
                 .format(LIGHT_RED, COLOUR_RESET))
    else:
        sys.exit("\n{0}ERROR: An unknown error occurred. Exiting.{1}\n"
                 .format(LIGHT_RED, COLOUR_RESET))

#############
# Kickstart #
#############

# Load Main Menu only if an active Internet connection is present.
if check_network_connection():
    linux_setup_menu()
elif not check_network_connection():
    sys.exit("\n{0}ERROR: Network connection not available. Exiting.{1}\n"
             .format(LIGHT_RED, COLOUR_RESET))
else:
    sys.exit("\n{0}ERROR: An unknown error occurred. Exiting.{1}\n"
             .format(LIGHT_RED, COLOUR_RESET))

# End of File.
