#!/usr/bin/env python3

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

"""
Script Name: minebackup.py
Script Author: William Whinn

Create a tarball containing save data and screenshots for Minecraft:
Java Edition within the user's home folder and provide a SHA512SUM
file.
"""

###########
# Imports #
###########

import datetime
import os
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata
SCRIPT_VERSION = '0.0.1'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell_scripts'

# String Colours
GREEN = '\033[0;92m'
RED = '\033[0;91m'
YELLOW = '\033[0;93m'

RESET = '\033[0;m'

# Paths
HOME = os.environ['HOME']

#############
# Functions #
#############

def minebackup_main():
    """Main function wrapper for 'minebackup.py' script."""

    # Inform the user to wait while process completes.
    print("\nNow creating {0}Minecraft: Java Edition{1} backup. Please Wait.\n"
          .format(GREEN, RESET))

    # Generate date-stamped filename and assign to variable.
    archive_name = minebackup_create_archive()

    # Create a matching SHA512SUM file for the above archive.
    minebackup_create_checksum(archive_name)

    # Insert final newline.
    print()

    return 0


def minebackup_create_archive():
    """Create a tarball containing Minecraft: Java Edition save data."""

    # Minecraft paths
    minecraft_folder = "{0}/.minecraft".format(HOME)
    saves = "{0}/saves".format(minecraft_folder)
    screenshots = "{0}/screenshots".format(minecraft_folder)

    # Create current datestamp for tarball filename.
    now = datetime.datetime.now()
    current_time = "{:04d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z".format(now.year,
                                                                   now.month,
                                                                   now.day,
                                                                   now.hour,
                                                                   now.minute,
                                                                   now.second)

    # Create formatted archive name including datestamp.
    archive_name = "Minecraft_{0}.tar.gz".format(current_time)

    # Define 'tar' compression command.
    tar_command = ('cd; tar -czf "{0}" "{1}" "{2}" --absolute-names; cd ~-'
                   .format(archive_name, saves, screenshots))

    # - Create Minecraft save data tarball if '~/.minecraft' folder
    #   exists and is not empty.
    if os.path.isdir(minecraft_folder) and os.listdir(minecraft_folder):
        # Create the archive.
        subprocess.run(tar_command, shell=True, check=True)

        # Inform the user of archive creation.
        print("Created TAR archive {0}~/{1}{2}.".format(YELLOW,
                                                        archive_name,
                                                        RESET))
    else:
        sys.exit("\n{0}ERROR: Minecraft data folder not found.{1}\n"
                 .format(RED, RESET))

    return archive_name


def minebackup_create_checksum(archive_name):
    """Create a SHA512SUM hash of the Minecraft save data tarball."""

    # Define SHA512SUM file.
    sha512sum_file = "{0}".format(archive_name).replace(".tar.gz",
                                                        ".sha512sum")

    # Define SHA512SUM command.
    sha512sum_command = ("cd; sha512sum {0} > {1}; cd ~-"
                         .format(archive_name, sha512sum_file))

    # Check archive exists before continuing.
    if os.path.isfile("{0}/{1}".format(HOME, archive_name)):
        subprocess.run(sha512sum_command, shell=True, check=True)

        # Inform the user that the file has been created.
        print("Created SHA512SUM file {0}~/{1}{2}.".format(YELLOW,
                                                         sha512sum_file,
                                                         RESET))
    else:
        # Archive tarball was not found.
        sys.exit("{0}ERROR: Minecraft save data tarball not found.{1}"
                 .format(RED, RESET))

    return 0


#############
# Kickstart #
#############

minebackup_main()

# End of File.
