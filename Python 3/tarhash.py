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
Script Name: tarhash.py
Script Author: William Whinn

Create a tarball of a given directory and provide a matching SHA512SUM
checksum file.
"""

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
SCRIPT_VERSION = '0.0.1'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell_scripts'

# String Colours
GREEN = '\033[0;92m'
RED = '\033[0;91m'
YELLOW = '\033[0;93m'

RESET = '\033[0;m'

#############
# Functions #
#############

def tarhash_main():
    """Main function wrapper for 'tarhash.py'."""

    # Success: Correct number of arguments.
    if len(sys.argv) == 2:

        # Display help and exit.
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            tarhash_help()

        # Show version information and exit.
        elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
            tarhash_version()

        # - Create tarball of directory and sha512sum file of the
        #   tarball.
        else:
            archive = tarhash_create_archive("".join(sys.argv[1]))
            tarhash_create_sha512sum(archive)

    # Failure: Too many arguments.
    elif len(sys.argv) > 2:
        sys.exit("\n{0}ERROR: Too many arguments provided.{1}\n"
                 .format(RED, RESET))

    return 0


def tarhash_create_archive(directory):
    """Create a tarball of a given directory."""

    # Construct archive filename.
    archive = "{0}.tar.gz".format(directory)

    # Construct tar command.
    tar_command = "tar -czf '{0}' '{1}' --absolute-names".format(archive,
                                                                 directory)

    # Error: Target does not exist.
    if not os.path.exists(directory):
        sys.exit("\n{0}ERROR: Target does not exist.{1}\n"
                 .format(RED, RESET))

    # Error: Cannot create archive from current working directory.
    elif directory == ".":
        sys.exit("\n{0}ERROR: Current directory is invalid.{1}\n"
                 .format(RED, RESET))

    # Error: Target is a file.
    elif os.path.isfile(directory):
        sys.exit("\n{0}ERROR: Target must be a directory.{1}\n"
                 .format(RED, RESET))

    elif not os.listdir(directory):
        sys.exit("\n{0}ERROR: Target must not be empty.{1}\n"
                 .format(RED, RESET))

    # Success: Target is a directory.
    elif os.path.isdir(directory):

        # Inform the user.
        print("tarhash v{0} compressing {1}{2}{3}. Please wait."
              .format(SCRIPT_VERSION,
                      YELLOW,
                      directory,
                      RESET))

        # Execute compiled command.
        subprocess.run(tar_command, shell=True, check=True)

        # Inform the user.
        print("Created tarball file {0}{1}{2}.".format(GREEN,
                                                       archive,
                                                       RESET))

    # Error: Catch all.
    else:
        sys.exit("\n{0}ERROR: An unknown error occurred.{1}\n"
                 .format(RED, RESET))

    return archive


def tarhash_create_sha512sum(archive):
    """Create a SHA512SUM file of a given tarball."""

    # Define filename for SHA512SUM checksum file.
    sha512sum_file = archive.replace(".tar.gz", ".sha512sum")

    # Compile SHA512SUM command.
    sha512sum_command = "sha512sum {0} > {1}".format(archive, sha512sum_file)

    # Success: File exists and is a file.
    if os.path.isfile(archive):

        # Execute compiled command.
        subprocess.run(sha512sum_command, shell=True, check=True)

        # Inform the user.
        print("Created checksum file {0}{1}{2}.".format(GREEN,
                                                        sha512sum_file,
                                                        RESET))

    # Error: Catch all.
    else:
        sys.exit("\n{0}ERROR: An unknown error occurred.{1}\n"
                 .format(RED, RESET))

    return 0


def tarhash_help():
    """Show help information and exit."""

    print("Usage: tarhash [OPTION/DIRECTORY]\n",
          "-h, --help\t\tDisplay this help and exit.",
          "-v, --version\t\tDisplay version information.\n", sep="\n")

    return 0


def tarhash_version():
    """Show version information and exit."""

    print("tarhash v{0}".format(SCRIPT_VERSION),
          "Copyright (C) 2021 William Whinn",
          "{0}\n".format(SCRIPT_URL), sep="\n")

    return 0


#############
# Kickstart #
#############

tarhash_main()

# End of File.
