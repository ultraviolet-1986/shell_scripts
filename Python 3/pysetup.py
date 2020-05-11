#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manage and maintain your Linux installation"""

###########
# Imports #
###########

import os
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata
SCRIPT_VERSION = '0.1.0'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell-scripts'

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
FLATPAK = '/usr/bin/flatpak'
SNAP = '/usr/bin/snap'

# Anaconda (User-Installed)
ANACONDA = "{0}/anaconda3/bin/anaconda".format(HOME)
CONDA = "{0}/anaconda3/bin/conda".format(HOME)

#############
# Functions #
#############

def clear():
    """Clear the current Terminal window"""
    os.system('clear')


def linux_setup_menu():
    """Clear the screen and display the main menu"""

    clear()

    print('{0}Linux System Maintenance Utility {1}{2}'.format(BOLD,
                                                              SCRIPT_VERSION,
                                                              COLOUR_RESET))
    print('Copyright (C) 2020 William Whinn')
    print("{0}\n".format(SCRIPT_URL))

    # Display Main Menu
    print('  {0}1.{1} Update System Software'.format(LIGHT_GREEN,
                                                     COLOUR_RESET))
    print()
    print('  {0}X.{1} Exit Program\n'.format(LIGHT_RED, COLOUR_RESET))

    answer = input("Please enter your selection: ")

    if answer == '1':
        clear()
        update_system_software()
    elif answer in ('X', 'x'):
        clear()
        sys.exit()
    else:
        print()
        sys.exit('ERROR: Incorrect response\n')


def update_system_software():
    """Detect various package managers and update system software"""

    # Main system package managers (DNF, APT, etc.)
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
    else:
        pass

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

    print("{0}System software has been updated.{1}\n".format(LIGHT_GREEN,
                                                             COLOUR_RESET))


#############
# Kickstart #
#############

linux_setup_menu()

# End of File.
