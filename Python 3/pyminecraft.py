#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download the Minecraft game launcher for GNU/Linux from Microsoft/Mojang and
create a mountable .iso disk image.
"""

###########
# Imports #
###########

import os
import shutil
import socket
import subprocess
import sys
import tarfile
import urllib.request

#############
# Variables #
#############

GREEN = '\x1b[0;32m'
RED = '\x1b[0;31m'
YELLOW = '\x1b[0;33m'
RESET = '\033[0;m'

MINECRAFT_URL = 'https://launcher.mojang.com/download/Minecraft.tar.gz'

HOME = os.environ['HOME']
DOWNLOADS = "{0}/Downloads".format(HOME)

WGET_PATH = '/usr/bin/wget'
MKISOFS_PATH = '/usr/bin/mkisofs'

#############
# Functions #
#############

def check_network_connection():
    """Detect whether or not an active Internet connection is available."""

    try:
        socket.create_connection(('1.1.1.1', 80))
        return True
    except OSError:
        return False

def remove_minecraft_data():
    """Delete data which are not part of the final .iso image."""

    print("Removing old Minecraft Launcher data...")

    if os.path.exists("{0}/minecraft.tar.gz".format(DOWNLOADS)):
        os.remove("{0}/minecraft.tar.gz".format(DOWNLOADS))
        print("Deleted old 'minecraft.tar.gz' file.")

    if os.path.exists("{0}/Minecraft".format(DOWNLOADS)):
        shutil.rmtree("{0}/Minecraft".format(DOWNLOADS))
        print("Deleted old 'Minecraft' directory.")

    if os.path.exists("{0}/minecraft-launcher".format(DOWNLOADS)):
        shutil.rmtree("{0}/minecraft-launcher".format(DOWNLOADS))
        print("Deleted old 'minecraft-launcher' directory.")

def download_minecraft_data():
    """Download minecraft data and compile a mountable .iso image file."""

    # Terminate if dependency 'genisoimage' is not installed.
    if not os.path.exists(MKISOFS_PATH):
        sys.exit("{0}ERROR: Program dependency 'genisoimage' not installed.{1}"
                 .format(RED, RESET))

    remove_minecraft_data()

    # Download the 'minecraft.tar.gz' file.
    print("Downloading Minecraft launcher archive...")
    urllib.request.urlretrieve(MINECRAFT_URL, "{0}/minecraft.tar.gz"
                               .format(DOWNLOADS))

    # Extract the contents of 'minecraft.tar.gz'.
    print("Extracting Minecraft launcher archive...")
    archive = tarfile.open("{0}/minecraft.tar.gz".format(DOWNLOADS))
    archive.extractall("{0}".format(DOWNLOADS))

    # Inject 'autorun.sh' file.
    print("Injecting 'autorun.sh' file...")
    autorun = open("{0}/minecraft-launcher/autorun.sh".format(DOWNLOADS), "w")
    autorun.write("{0}\n\n{1}\n\n{2}\n".format("#!/usr/bin/env bash",
                                               "./minecraft-launcher",
                                               "# End of File."))
    autorun.close()

    # Make 'autorun.sh' executable.
    print("Making 'autorun.sh' file executable...")
    os.chmod("{0}/minecraft-launcher/autorun.sh".format(DOWNLOADS), 0o755)

    # Remove previous build of 'Minecraft.iso' file if exists.
    if os.path.exists("{0}/Minecraft.iso".format(DOWNLOADS)):
        os.remove("{0}/Minecraft.iso".format(DOWNLOADS))
        print("Deleted old 'Minecraft.iso' file.")

    # Create the .iso Disk Image.
    mkisofs_command = ("mkisofs -volid 'Minecraft' -o '{0}/Minecraft.iso' "
                       "-input-charset UTF-8 -joliet -joliet-long "
                       "-rock '{0}/minecraft-launcher' > /dev/null 2>&1"
                       .format(DOWNLOADS))
    print("Building '{0}/Minecraft.iso' disk image...".format(DOWNLOADS))
    subprocess.run(mkisofs_command, shell=True, check=True)

    # Cleanup the Download folder.
    remove_minecraft_data()

#############
# Kickstart #
#############

if check_network_connection():
    download_minecraft_data()
elif not check_network_connection():
    sys.exit("\n{0}ERROR: Network connection not available. Exiting.{1}\n"
             .format(RED, RESET))
else:
    sys.exit("\n{0}ERROR: An unknown error occurred. Exiting.{1}\n"
             .format(RED, RESET))

# End of File.
