#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create a mountable ISO disk image of a given folder.
"""

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
    package installed.
    """

    basename = target.split('/')[-1]
    current_directory = os.environ['PWD']

    genisofs_command = (
        'mkisofs -volid "{0}" -output "{1}/{2}.iso" -input-charset UTF-8 -udf '
        '-allow-limited-size -disable-deep-relocation -untranslated-filenames '
        '"{3}" '.format(str(generate_disk_label()), current_directory,
                        basename, target))

    try:
        if os.path.isdir(target):
            subprocess.run(genisofs_command, shell=True, check=True)
        elif not os.path.isdir(target):
            print("ERROR: The target does not exist.")
        else:
            print("ERROR: An unknown error occurred.")
    except OSError as error:
        if error.errno == errno.ENOENT:
            pass
        else:
            raise

#############
# Kickstart #
#############

create_disk_image(''.join(sys.argv[1:]))

# End of File.
