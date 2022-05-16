#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create a compressed backup of the user's 'Home' folder."""

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

###########
# Imports #
###########

import datetime
import glob
import os
import subprocess
import sys

#############
# Variables #
#############

# Script Metadata
SCRIPT_VERSION = '0.2.3'
SCRIPT_URL = 'https://github.com/ultraviolet-1968/shell_scripts'

# String Colors
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

# String Formatting
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

COLOUR_RESET = '\033[0;m'

# Linux Environmental Variables
DESKTOP = os.environ['XDG_CURRENT_DESKTOP']
HOME = os.environ['HOME']
HOSTNAME = os.environ['HOSTNAME'].upper()
USER = os.environ['USER']

#############
# Functions #
#############


def clear():
    """Clear the current Terminal window."""
    os.system('clear')


def backup_dconf_settings():
    """Create a file containing common GTK desktop settings."""
    dconf_dump_file = 'dconf_dump.txt'
    dconf_dump_command = f'dconf dump / > {BACKUP}/{dconf_dump_file}'

    if DESKTOP != 'KDE':
        subprocess.run(dconf_dump_command, shell=True, check=True)
        print(f'Created Settings File {YELLOW}{BACKUP}/{dconf_dump_file}{COLOUR_RESET}.')


def backup_folder(archive_name, folder_to_compress):
    """Create a compressed archive of a target folder."""
    now = datetime.datetime.now()
    date = f"{now.year:04d}{now.month:02d}{now.day:02d}"
    timestamp = f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
    current_time = f"{date}T{timestamp}Z"

    if os.path.exists(folder_to_compress) and os.path.isdir(folder_to_compress):
        if os.listdir(folder_to_compress):
            subprocess.run(f'zip -q -r "{archive_name}_{current_time}.zip" "{folder_to_compress}"',
                           shell=True, check=True)
            print(f'Created Archive {YELLOW}{archive_name}_{current_time}.zip{COLOUR_RESET}.')


def create_checksum():
    """Create a SHA512 checksum of the BACKUP archive(s)."""
    if glob.glob(f'{BACKUP}/*.zip'):
        sha512sum_file = 'BACKUP.sha512sum'
        sha512sum_command = f'cd {BACKUP}; sha512sum *.zip > "{BACKUP}/{sha512sum_file}"; cd ~-'

        subprocess.run(sha512sum_command, shell=True, check=True)
        print(f'Created Checksum {YELLOW}{BACKUP}/{sha512sum_file}{COLOUR_RESET}.')
    else:
        pass

#############
# Kickstart #
#############

clear()

# Display script header.
print(f'{BOLD}Linux Home Folder Backup Utility {SCRIPT_VERSION}{COLOUR_RESET}')
print('Copyright (C) 2020 William Whinn')
print(f"{SCRIPT_URL}\n")

# Select Backup Location.
print(f'  {LIGHT_GREEN}1.{COLOUR_RESET} Local Disk (Home Folder)')
print(f'  {LIGHT_GREEN}2.{COLOUR_RESET} External Media (Hostname as Disk Label)\n')
print(f'  {LIGHT_RED}X.{COLOUR_RESET} Exit Program\n')

ANSWER = input("Please enter your selection: ")

if ANSWER == '1':
    print()
    BACKUP = f'{HOME}/Backup_{HOSTNAME}'
elif ANSWER == '2':
    print()
    BACKUP = f'/run/media/{USER}/{HOSTNAME}/Backup_{1}'
elif ANSWER in ('X', 'x'):
    clear()
    sys.exit()
else:
    print()
    sys.exit(f"{LIGHT_RED}ERROR: Incorrect response{COLOUR_RESET}\n")

# Create Backup Location.
if not os.path.exists(BACKUP):
    os.makedirs(BACKUP)

clear()
print(f"{LIGHT_YELLOW}Now performing backup of Home Folder data. Please Wait...{COLOUR_RESET}\n")

# Record GTK-based desktop settings.
backup_dconf_settings()

# Home 'bin' folder.
BIN_DATA_FOLDER = f'{HOME}/bin'
BIN_DATA_ARCHIVE = f'{BACKUP}/bin'
backup_folder(BIN_DATA_ARCHIVE, BIN_DATA_FOLDER)

# Backup Dwarf Fortress (Snap).
DF_DATA_FOLDER = f'{HOME}/snap/dwarffortress'
DF_DATA_ARCHIVE = f'{BACKUP}/DwarfFortressSnap'
backup_folder(DF_DATA_ARCHIVE, DF_DATA_FOLDER)

# Backup GIMP (Flatpak).
GIMP_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gimp.GIMP'
GIMP_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GIMPFlatpakBackup'
backup_folder(GIMP_FLATPAK_DATA_ARCHIVE, GIMP_FLATPAK_DATA_FOLDER)

# Backup GNOME Calculator (Flatpak).
GNOMECALC_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.Calculator'
GNOMECALC_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GNOMECalculatorFlatpakBackup'
backup_folder(GNOMECALC_FLATPAK_DATA_ARCHIVE, GNOMECALC_FLATPAK_DATA_FOLDER)

# Backup GNOME Calendar (Flatpak).
GNOMECALENDAR_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.Calendar'
GNOMECALENDAR_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GNOMECalendarFlatpakBackup'
backup_folder(GNOMECALENDAR_FLATPAK_DATA_ARCHIVE, GNOMECALENDAR_FLATPAK_DATA_FOLDER)

# Backup GNOME Clocks (Flatpak).
GNOMECLOCKS_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.clocks'
GNOMECLOCKS_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GNOMEClocksFlatpakBackup'
backup_folder(GNOMECLOCKS_FLATPAK_DATA_ARCHIVE, GNOMECLOCKS_FLATPAK_DATA_FOLDER)

# Backup GNOME Contacts (Flatpak).
GNOMECONTACTS_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.Contacts'
GNOMECONTACTS_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GNOMEContactsFlatpakBackup'
backup_folder(GNOMECONTACTS_FLATPAK_DATA_ARCHIVE, GNOMECONTACTS_FLATPAK_DATA_FOLDER)

# Backup Evince (Flatpak).
EVINCE_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.Evince'
EVINCE_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/EvinceFlatpakBackup'
backup_folder(EVINCE_FLATPAK_DATA_ARCHIVE, EVINCE_FLATPAK_DATA_FOLDER)

# Backup Evolution (Flatpak).
EVOLUTION_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.Evolution'
EVOLUTION_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/EvolutionFlatpakBackup'
backup_folder(EVOLUTION_FLATPAK_DATA_ARCHIVE, EVOLUTION_FLATPAK_DATA_FOLDER)

# Backup Firefox (Flatpak).
FIREFOX_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.mozilla.firefox'
FIREFOX_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/FirefoxFlatpakBackup'
backup_folder(FIREFOX_FLATPAK_DATA_ARCHIVE, FIREFOX_FLATPAK_DATA_FOLDER)

# Backup GEdit (Flatpak).
GEDIT_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.gnome.gedit'
GEDIT_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/GEditFlatpakBackup'
backup_folder(GEDIT_FLATPAK_DATA_ARCHIVE, GEDIT_FLATPAK_DATA_FOLDER)

# Backup Inkscape (Flatpak).
INKSCAPE_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.inkscape.Inkscape'
INKSCAPE_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/InkscapeFlatpakBackup'
backup_folder(INKSCAPE_FLATPAK_DATA_ARCHIVE, INKSCAPE_FLATPAK_DATA_FOLDER)

# Backup LibreOffice (Flatpak).
LIBREOFFICE_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.libreoffice.LibreOffice'
LIBREOFFICE_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/LibreofficeFlatpakBackup'
backup_folder(LIBREOFFICE_FLATPAK_DATA_ARCHIVE, LIBREOFFICE_FLATPAK_DATA_FOLDER)

# Backup Minecraft.
MINECRAFT_DATA_FOLDER = f'{HOME}/.minecraft'
MINECRAFT_DATA_ARCHIVE = f'{BACKUP}/Minecraft'
backup_folder(MINECRAFT_DATA_ARCHIVE, MINECRAFT_DATA_FOLDER)

# Backup Minecraft (Flatpak).
MINECRAFT_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/com.mojang.Minecraft'
MINECRAFT_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/MinecraftFlatpakBackup'
backup_folder(MINECRAFT_FLATPAK_DATA_ARCHIVE, MINECRAFT_FLATPAK_DATA_FOLDER)

# Backup MultiMC (DEB Package).
MULTIMC_DATA_FOLDER = f'{HOME}/.local/share/multimc'
MULTIMC_DATA_ARCHIVE = f'{BACKUP}/MultiMCBackup'
backup_folder(MULTIMC_DATA_ARCHIVE, MULTIMC_DATA_FOLDER)

# Backup Notes.
DOCUMENTS_DATA_FOLDER = f'{HOME}/Documents/Notes'
DOCUMENTS_DATA_ARCHIVE = f'{BACKUP}/NotesBackup'
backup_folder(DOCUMENTS_DATA_ARCHIVE, DOCUMENTS_DATA_FOLDER)

# Backup NotesUp.
NOTESUP_DATA_FOLDER = f'{HOME}/.local/share/notes-up'
NOTESUP_DATA_ARCHIVE = f'{BACKUP}/NotesUpData'
backup_folder(NOTESUP_DATA_ARCHIVE, NOTESUP_DATA_FOLDER)

# Backup Pictures.
PICTURES_DATA_FOLDER = f'{HOME}/Pictures'
PICTURES_DATA_ARCHIVE = f'{BACKUP}/Pictures'
backup_folder(PICTURES_DATA_ARCHIVE, PICTURES_DATA_FOLDER)

# Backup R Libraries.
R_DATA_FOLDER = f'{HOME}/R'
R_DATA_ARCHIVE = f'{BACKUP}/RLibraries'
backup_folder(R_DATA_ARCHIVE, R_DATA_FOLDER)

# Backup Ren'Py.
RENPY_SAVE_DATA_FOLDER = f'{HOME}/.renpy'
RENPY_SAVE_DATA_ARCHIVE = f'{BACKUP}/RenPySaveData'
backup_folder(RENPY_SAVE_DATA_ARCHIVE, RENPY_SAVE_DATA_FOLDER)

# Backup RetroArch (Flatpak).
RETROARCH_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.libretro.RetroArch'
RETROARCH_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/RetroArchFlatpakBackup'
backup_folder(RETROARCH_FLATPAK_DATA_ARCHIVE, RETROARCH_FLATPAK_DATA_FOLDER)

# Backup RetroArch (Snap).
RETROARCH_DATA_FOLDER = f'{HOME}/snap/retroarch'
RETROARCH_DATA_ARCHIVE = f'{BACKUP}/RetroArchSnap'
backup_folder(RETROARCH_DATA_ARCHIVE, RETROARCH_DATA_FOLDER)

# Backup ScummVM.
SCUMMVM_DATA_FOLDER = f'{HOME}/.local/share/scummvm'
SCUMMVM_DATA_ARCHIVE = f'{BACKUP}/ScummVMBackup'
backup_folder(SCUMMVM_DATA_ARCHIVE, SCUMMVM_DATA_FOLDER)

# Backup ScummVM (Flatpak).
SCUMMVM_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.scummvm.ScummVM'
SCUMMVM_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/ScummVMFlatpakBackup'
backup_folder(SCUMMVM_FLATPAK_DATA_ARCHIVE, SCUMMVM_FLATPAK_DATA_FOLDER)

# Backup SSH Keys.
SSHKEYS_DATA_FOLDER = f'{HOME}/.ssh'
SSHKEYS_DATA_ARCHIVE = f'{BACKUP}/SSHKeys'
backup_folder(SSHKEYS_DATA_ARCHIVE, SSHKEYS_DATA_FOLDER)

# Backup Templates.
TEMPLATES_DATA_FOLDER = f'{HOME}/Templates'
TEMPLATES_DATA_ARCHIVE = f'{BACKUP}/Templates'
backup_folder(TEMPLATES_DATA_ARCHIVE, TEMPLATES_DATA_FOLDER)

# Backup Mozilla Thunderbird.
THUNDERBIRD_DATA_FOLDER = f'{HOME}/.thunderbird'
THUNDERBIRD_DATA_ARCHIVE = f'{BACKUP}/Thunderbird'
backup_folder(THUNDERBIRD_DATA_ARCHIVE, THUNDERBIRD_DATA_FOLDER)

# Backup VLC (Flatpak).
VLC_FLATPAK_DATA_FOLDER = f'{HOME}/.var/app/org.videolan.VLC'
VLC_FLATPAK_DATA_ARCHIVE = f'{BACKUP}/VLCFlatpakBackup'
backup_folder(VLC_FLATPAK_DATA_ARCHIVE, VLC_FLATPAK_DATA_FOLDER)

# Backup Workspace.
DOCUMENTS_DATA_FOLDER = f'{HOME}/Documents/Workspace'
DOCUMENTS_DATA_ARCHIVE = f'{BACKUP}/WorkspaceBackup'
backup_folder(DOCUMENTS_DATA_ARCHIVE, DOCUMENTS_DATA_FOLDER)

create_checksum()

# Final newline.
sys.exit(f"\n{LIGHT_GREEN}Files have been backed up to {BACKUP}.{COLOUR_RESET}\n")

# End of File.
