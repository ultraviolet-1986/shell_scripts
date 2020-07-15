#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create an encrypted backup of a target file, or decrypt an encrypted file using GnuPG from package
'gnupg2'.
"""

###########
# License #
###########

# Shell Scripts: A collection of shell scripts in various languages.
# Copyright (C) 2020 William Willis Whinn

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not,
# see <http://www.gnu.org/licenses/>.

###########
# Imports #
###########

import argparse
import errno
import os
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata
SCRIPT_VERSION = '0.0.2'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell_scripts'

# Command-line arguments.
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-e', '--encrypt', help="GnuPG encrypt a target file.")
PARSER.add_argument('-d', '--decrypt', help="GnuPG decrypt a target file.")

# Executable Paths.
GPG_PATH = '/usr/bin/gpg'

# Text Formatting.
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
RESET = '\033[0;m'

#############
# Functions #
#############

def gpg_encrypt_file(target):
    """Create a GnuPG encrypted file."""
    try:
        if os.path.exists(target):
            subprocess.run("gpg --symmetric {0}".format(target), shell=True, check=True)
            sys.exit("{0}SUCCESS: File '{1}' has been encrypted.{2}".format(GREEN, target, RESET))
        elif not os.path.exists(target):
            sys.exit("{0}ERROR: File '{1}' does not exist.{2}".format(RED, target, RESET))
        else:
            sys.exit("{0}ERROR: An unknown error occurred.{1}".format(RED, RESET))
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise


def gpg_decrypt_file(target):
    """Decrypt a GnuPG encrypted file."""

    decrypted_file_basename = "{0}".format(os.path.splitext(target)[0])

    try:
        if os.path.exists(target):
            subprocess.run('gpg --output "{0}" --decrypt "{1}"'.format(decrypted_file_basename,
                                                                       target),
                           shell=True, check=True)
            sys.exit("{0}SUCCESS: File '{1}' has been decrypted.{2}".format(GREEN, target, RESET))
        elif not os.path.exists(target):
            sys.exit("{0}ERROR: File '{1}' does not exist.{2}".format(RED, target, RESET))
        else:
            sys.exit("{0}ERROR: An unknown error occurred.{1}".format(RED, RESET))
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise

#############
# Kickstart #
#############

# Parse command-line arguments.
ARGS = PARSER.parse_args()

# Pass command-line argument.
if not os.path.exists(GPG_PATH):
    sys.exit("{0}ERROR: Package 'gnupg2' is not installed.{1}".format(RED, RESET))
elif ARGS.encrypt:
    gpg_encrypt_file(ARGS.encrypt)
elif ARGS.decrypt:
    gpg_decrypt_file(ARGS.decrypt)
else:
    sys.exit("{0}ERROR: An argument was not provided.{1}".format(RED, RESET))

# End of File.
