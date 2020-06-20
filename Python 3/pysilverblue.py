#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manage default Flatpak software or replace with RPM equivalents."""

###########
# Imports #
###########

import errno
import os
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata

SCRIPT_VERSION = '0.0.1'
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

# Software Lists

FLATPAK_SOFTWARE = (
    "org.gnome.Baobab",
    "org.gnome.Calculator",
    "org.gnome.Characters",
    "org.gnome.Evince",
    "org.gnome.FileRoller",
    "org.gnome.Logs",
    "org.gnome.Screenshot",
    "org.gnome.clocks",
    "org.gnome.eog",
    "org.gnome.font-viewer",
    "org.gnome.gedit"
)

RPM_SOFTWARE = (
    "automake",
    "baobab",
    "clamav",
    "clamav-update",
    "code",
    "eog",
    "evince",
    "evolution",
    "exfat-utils",
    "ffmpeg",
    "file-roller",
    "fuse-exfat",
    "gcc",
    "gcc-c++",
    "gedit",
    "genisoimage",
    "gnome-calculator",
    "gnome-characters",
    "gnome-clocks",
    "gnome-font-viewer",
    "gnome-logs",
    "gnome-screenshot",
    "gnome-tweaks",
    "make",
    "mpv",
    "skypeforlinux",
    "transmission",
    "vim"
)

RPM_SOFTWARE = ' '.join(RPM_SOFTWARE)

#############
# Functions #
#############

def clear():
    """Clear the current Terminal window."""
    os.system('clear')


def silverblue_setup_menu():
    """Display the program's main menu."""
    clear()

    print("{0}Fedora Silverblue Setup Menu {1}{2}".format(BOLD,
                                                          SCRIPT_VERSION,
                                                          COLOUR_RESET))
    print("Copyright (C) 2020 William Whinn")
    print("{0}".format(SCRIPT_URL))

    print()
    print("  {0}1.{1} Install RPM Software".format(GREEN, COLOUR_RESET))
    print("  {0}2.{1} Remove RPM Software".format(GREEN, COLOUR_RESET))
    print("  {0}3.{1} Install Flatpak Software".format(GREEN, COLOUR_RESET))
    print("  {0}4.{1} Remove Flatpak Software".format(GREEN, COLOUR_RESET))
    print()
    print("  {0}X.{1} Exit Program".format(RED, COLOUR_RESET))
    print()

    answer = input("Please enter your selection: ")

    if answer == '1':
        clear()
        install_rpm_software()
    elif answer == '2':
        clear()
        remove_rpm_software()
    elif answer == '3':
        clear()
        install_flatpak_software()
    elif answer == '4':
        clear()
        remove_flatpak_software()
    elif answer in ('X', 'x'):
        clear()
        sys.exit()
    else:
        print()
        sys.exit("{0}ERROR: Incorrect Response.{1}\n".format(RED,
                                                             COLOUR_RESET))


def install_flatpak_software():
    """Install software defined within the 'FLATPAK_SOFTWARE' variable."""
    for i in FLATPAK_SOFTWARE:
        subprocess.run("flatpak install fedora -y {0}".format(i),
                       shell=True, check=True)


def remove_flatpak_software():
    """Remove software defined within the 'FLATPAK_SOFTWARE' variable."""
    for i in FLATPAK_SOFTWARE:
        subprocess.run("flatpak uninstall {0}".format(i),
                       shell=True, check=True)


def install_rpm_software():
    """Install software defined within the 'RPM_SOFTWARE' variable."""
    try:
        subprocess.run("rpm-ostree install {0}".format(RPM_SOFTWARE),
                       shell=True, check=True)
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise


def remove_rpm_software():
    """Remove software defined within the 'RPM_SOFTWARE' variable."""
    try:
        subprocess.run("rpm-ostree remove {0}".format(RPM_SOFTWARE),
                       shell=True, check=True)
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise

#############
# Kickstart #
#############

silverblue_setup_menu()

# End of File.
