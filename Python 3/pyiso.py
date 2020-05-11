#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create a mountable ISO disk image of a given folder."""

###########
# Imports #
###########

import errno
import os
import random
import string
import subprocess
import sys

#############
# Variables #
#############

MKISOFS = '/usr/bin/mkisofs'

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

#############
# Functions #
#############

def generate_disk_label():
    """Create two random alphanumeric strings and combine them."""

    label_1 = ''.join(random.choices(string.ascii_uppercase + string.digits,
                                     k=4))
    label_2 = ''.join(random.choices(string.ascii_uppercase + string.digits,
                                     k=4))
    label = "{0}-{1}".format(label_1, label_2)

    return label

def create_disk_image(target):
    """
    Create a UDF disk image (non IS0-9660 compliant). Requires 'genisoimage'
    package to be installed.
    """

    basename = target.split('/')[-1]
    current_directory = os.environ['PWD']

    genisofs_command = (
        'mkisofs -volid "{0}" -output "{1}/{2}.iso" -input-charset UTF-8 -udf '
        '-allow-limited-size -disable-deep-relocation -untranslated-filenames '
        '"{3}" '.format(str(generate_disk_label()), current_directory,
                        basename, target))

    try:
        if os.path.exists("{0}.iso".format(''.join(sys.argv[1:]))):
            sys.exit("\n{0}ERROR: The disk image already exists. Exiting.\n{1}"
                     .format(LIGHT_RED, COLOUR_RESET))
        elif not os.path.isdir(target):
            sys.exit("\n{0}ERROR: The target does not exist. Exiting.\n{1}"
                     .format(LIGHT_RED, COLOUR_RESET))
        elif os.path.isdir(target):
            subprocess.run(genisofs_command, shell=True, check=True)
        else:
            sys.exit("\n{0}ERROR: An unknown error occurred. Exiting.\n{1}"
                     .format(LIGHT_RED, COLOUR_RESET))
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise

#############
# Kickstart #
#############

if os.path.exists(MKISOFS):
    create_disk_image(''.join(sys.argv[1:]))
    print()
elif not os.path.exists(MKISOFS):
    sys.exit("\n{0}ERROR: Package 'genisofs' is not installed. Exiting.\n{1}"
             .format(LIGHT_RED, COLOUR_RESET))
else:
    sys.exit("\n{0}ERROR: An unknown error occurred. Exiting.\n{1}"
             .format(LIGHT_RED, COLOUR_RESET))

# End of File.
