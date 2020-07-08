#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create a compressed backup of the user's 'Home' folder."""

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
SCRIPT_VERSION = '0.2.2'
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
    dconf_dump_command = 'dconf dump / > {0}/{1}'.format(BACKUP, dconf_dump_file)

    if DESKTOP != 'KDE':
        subprocess.run(dconf_dump_command, shell=True, check=True)
        print('Created Settings File {0}{1}/{2}{3}.'.format(YELLOW,
                                                            BACKUP,
                                                            dconf_dump_file,
                                                            COLOUR_RESET))


def backup_folder(archive_name, folder_to_compress):
    """Create a compressed archive of a target folder."""
    now = datetime.datetime.now()
    current_time = "{:04d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z".format(now.year,
                                                                   now.month,
                                                                   now.day,
                                                                   now.hour,
                                                                   now.minute,
                                                                   now.second)

    if os.path.exists(folder_to_compress) and os.path.isdir(folder_to_compress):
        if os.listdir(folder_to_compress):
            subprocess.run('tar -czf "{0}_{1}.tar.gz" "{2}" --absolute-names'
                           .format(archive_name, current_time, folder_to_compress),
                           shell=True, check=True)
            print('Created Archive {0}{1}_{2}.tar.gz{3}.'.format(YELLOW,
                                                                 archive_name,
                                                                 current_time,
                                                                 COLOUR_RESET))


def create_checksum():
    """Create a SHA512 checksum of the BACKUP archive(s)."""
    if glob.glob('{0}/*.tar.gz'.format(BACKUP)):
        sha512sum_file = 'BACKUP.sha512sum'
        sha512sum_command = 'cd {0}; sha512sum *.tar.gz > "{0}/{1}"; cd ~-'.format(BACKUP,
                                                                                   sha512sum_file)

        subprocess.run(sha512sum_command, shell=True, check=True)
        print('Created Checksum {0}{1}/{2}{3}.'
              .format(YELLOW, BACKUP, sha512sum_file, COLOUR_RESET))
    else:
        pass

#############
# Kickstart #
#############

clear()

# Display script header.
print('{0}Linux Home Folder Backup Utility {1}{2}'.format(BOLD, SCRIPT_VERSION, COLOUR_RESET))
print('Copyright (C) 2020 William Whinn')
print("{0}\n".format(SCRIPT_URL))

# Select Backup Location.
print('  {0}1.{1} Local Disk (Home Folder)'.format(LIGHT_GREEN, COLOUR_RESET))
print('  {0}2.{1} External Media (Hostname as Disk Label)\n'.format(LIGHT_GREEN, COLOUR_RESET))
print('  {0}X.{1} Exit Program\n'.format(LIGHT_RED, COLOUR_RESET))

ANSWER = input("Please enter your selection: ")

if ANSWER == '1':
    print()
    BACKUP = '{0}/Backup_{1}'.format(HOME, HOSTNAME)
elif ANSWER == '2':
    print()
    BACKUP = '/run/media/{0}/{1}/Backup_{1}'.format(USER, HOSTNAME)
elif ANSWER in ('X', 'x'):
    clear()
    sys.exit()
else:
    print()
    sys.exit("{0}ERROR: Incorrect response{1}\n".format(LIGHT_RED, COLOUR_RESET))

# Create Backup Location.
if not os.path.exists(BACKUP):
    os.makedirs(BACKUP)

clear()
print("{0}Now performing backup of Home Folder data. Please Wait...{1}\n".format(LIGHT_YELLOW,
                                                                                 COLOUR_RESET))

# Record GTK-based desktop settings.
backup_dconf_settings()

# Backup Dwarf Fortress (Snap).
DF_DATA_FOLDER = '{0}/snap/dwarffortress'.format(HOME)
DF_DATA_ARCHIVE = '{0}/DwarfFortressSnap'.format(BACKUP)
backup_folder(DF_DATA_ARCHIVE, DF_DATA_FOLDER)

# Backup GIMP (Flatpak).
GIMP_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gimp.GIMP'.format(HOME)
GIMP_FLATPAK_DATA_ARCHIVE = '{0}/GIMPFlatpakBackup'.format(BACKUP)
backup_folder(GIMP_FLATPAK_DATA_ARCHIVE, GIMP_FLATPAK_DATA_FOLDER)

# Backup GNOME Calculator (Flatpak).
GNOMECALC_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.Calculator'.format(HOME)
GNOMECALC_FLATPAK_DATA_ARCHIVE = '{0}/GNOMECalculatorFlatpakBackup'.format(BACKUP)
backup_folder(GNOMECALC_FLATPAK_DATA_ARCHIVE, GNOMECALC_FLATPAK_DATA_FOLDER)

# Backup GNOME Calendar (Flatpak).
GNOMECALENDAR_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.Calendar'.format(HOME)
GNOMECALENDAR_FLATPAK_DATA_ARCHIVE = '{0}/GNOMECalendarFlatpakBackup'.format(BACKUP)
backup_folder(GNOMECALENDAR_FLATPAK_DATA_ARCHIVE, GNOMECALENDAR_FLATPAK_DATA_FOLDER)

# Backup GNOME Clocks (Flatpak).
GNOMECLOCKS_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.clocks'.format(HOME)
GNOMECLOCKS_FLATPAK_DATA_ARCHIVE = '{0}/GNOMEClocksFlatpakBackup'.format(BACKUP)
backup_folder(GNOMECLOCKS_FLATPAK_DATA_ARCHIVE, GNOMECLOCKS_FLATPAK_DATA_FOLDER)

# Backup GNOME Contacts (Flatpak).
GNOMECONTACTS_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.Contacts'.format(HOME)
GNOMECONTACTS_FLATPAK_DATA_ARCHIVE = '{0}/GNOMEContactsFlatpakBackup'.format(BACKUP)
backup_folder(GNOMECONTACTS_FLATPAK_DATA_ARCHIVE, GNOMECONTACTS_FLATPAK_DATA_FOLDER)

# Backup Evince (Flatpak).
EVINCE_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.Evince'.format(HOME)
EVINCE_FLATPAK_DATA_ARCHIVE = '{0}/EvinceFlatpakBackup'.format(BACKUP)
backup_folder(EVINCE_FLATPAK_DATA_ARCHIVE, EVINCE_FLATPAK_DATA_FOLDER)

# Backup Evolution (Flatpak).
EVOLUTION_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.Evolution'.format(HOME)
EVOLUTION_FLATPAK_DATA_ARCHIVE = '{0}/EvolutionFlatpakBackup'.format(BACKUP)
backup_folder(EVOLUTION_FLATPAK_DATA_ARCHIVE, EVOLUTION_FLATPAK_DATA_FOLDER)

# Backup Firefox (Flatpak).
FIREFOX_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.mozilla.firefox'.format(HOME)
FIREFOX_FLATPAK_DATA_ARCHIVE = '{0}/FirefoxFlatpakBackup'.format(BACKUP)
backup_folder(FIREFOX_FLATPAK_DATA_ARCHIVE, FIREFOX_FLATPAK_DATA_FOLDER)

# Backup GEdit (Flatpak).
GEDIT_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.gnome.gedit'.format(HOME)
GEDIT_FLATPAK_DATA_ARCHIVE = '{0}/GEditFlatpakBackup'.format(BACKUP)
backup_folder(GEDIT_FLATPAK_DATA_ARCHIVE, GEDIT_FLATPAK_DATA_FOLDER)

# Backup Inkscape (Flatpak).
INKSCAPE_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.inkscape.Inkscape'.format(HOME)
INKSCAPE_FLATPAK_DATA_ARCHIVE = '{0}/InkscapeFlatpakBackup'.format(BACKUP)
backup_folder(INKSCAPE_FLATPAK_DATA_ARCHIVE, INKSCAPE_FLATPAK_DATA_FOLDER)

# Backup LibreOffice (Flatpak).
LIBREOFFICE_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.libreoffice.LibreOffice'.format(HOME)
LIBREOFFICE_FLATPAK_DATA_ARCHIVE = '{0}/LibreofficeFlatpakBackup'.format(BACKUP)
backup_folder(LIBREOFFICE_FLATPAK_DATA_ARCHIVE, LIBREOFFICE_FLATPAK_DATA_FOLDER)

# Backup Minecraft.
MINECRAFT_DATA_FOLDER = '{0}/.minecraft'.format(HOME)
MINECRAFT_DATA_ARCHIVE = '{0}/Minecraft'.format(BACKUP)
backup_folder(MINECRAFT_DATA_ARCHIVE, MINECRAFT_DATA_FOLDER)

# Backup MultiMC (DEB Package).
MULTIMC_DATA_FOLDER = '{0}/.local/share/multimc'.format(HOME)
MULTIMC_DATA_ARCHIVE = '{0}/MultiMCBackup'.format(BACKUP)
backup_folder(MULTIMC_DATA_ARCHIVE, MULTIMC_DATA_FOLDER)

# Backup Notes.
DOCUMENTS_DATA_FOLDER = '{0}/Documents/Notes'.format(HOME)
DOCUMENTS_DATA_ARCHIVE = '{0}/NotesBackup'.format(BACKUP)
backup_folder(DOCUMENTS_DATA_ARCHIVE, DOCUMENTS_DATA_FOLDER)

# Backup NotesUp.
NOTESUP_DATA_FOLDER = '{0}/.local/share/notes-up'.format(HOME)
NOTESUP_DATA_ARCHIVE = '{0}/NotesUpData'.format(BACKUP)
backup_folder(NOTESUP_DATA_ARCHIVE, NOTESUP_DATA_FOLDER)

# Backup Pictures.
PICTURES_DATA_FOLDER = '{0}/Pictures'.format(HOME)
PICTURES_DATA_ARCHIVE = '{0}/Pictures'.format(BACKUP)
backup_folder(PICTURES_DATA_ARCHIVE, PICTURES_DATA_FOLDER)

# Backup R Libraries.
R_DATA_FOLDER = '{0}/R'.format(HOME)
R_DATA_ARCHIVE = '{0}/RLibraries'.format(BACKUP)
backup_folder(R_DATA_ARCHIVE, R_DATA_FOLDER)

# Backup Ren'Py.
RENPY_SAVE_DATA_FOLDER = '{0}/.renpy'.format(HOME)
RENPY_SAVE_DATA_ARCHIVE = '{0}/RenPySaveData'.format(BACKUP)
backup_folder(RENPY_SAVE_DATA_ARCHIVE, RENPY_SAVE_DATA_FOLDER)

# Backup RetroArch (Snap).
RETROARCH_DATA_FOLDER = '{0}/snap/retroarch'.format(HOME)
RETROARCH_DATA_ARCHIVE = '{0}/RetroArchSnap'.format(BACKUP)
backup_folder(RETROARCH_DATA_ARCHIVE, RETROARCH_DATA_FOLDER)

# Backup ScummVM.
SCUMMVM_DATA_FOLDER = '{0}/.local/share/scummvm'.format(HOME)
SCUMMVM_DATA_ARCHIVE = '{0}/ScummVMBackup'.format(BACKUP)
backup_folder(SCUMMVM_DATA_ARCHIVE, SCUMMVM_DATA_FOLDER)

# Backup ScummVM (Flatpak).
SCUMMVM_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.scummvm.ScummVM'.format(HOME)
SCUMMVM_FLATPAK_DATA_ARCHIVE = '{0}/ScummVMFlatpakBackup'.format(BACKUP)
backup_folder(SCUMMVM_FLATPAK_DATA_ARCHIVE, SCUMMVM_FLATPAK_DATA_FOLDER)

# Backup SSH Keys.
SSHKEYS_DATA_FOLDER = '{0}/.ssh'.format(HOME)
SSHKEYS_DATA_ARCHIVE = '{0}/SSHKeys'.format(BACKUP)
backup_folder(SSHKEYS_DATA_ARCHIVE, SSHKEYS_DATA_FOLDER)

# Backup Templates.
TEMPLATES_DATA_FOLDER = '{0}/Templates'.format(HOME)
TEMPLATES_DATA_ARCHIVE = '{0}/Templates'.format(BACKUP)
backup_folder(TEMPLATES_DATA_ARCHIVE, TEMPLATES_DATA_FOLDER)

# Backup Visual Studio Code (Flatpak).
VSCODE_FLATPAK_DATA_FOLDER = '{0}/.var/app/com.visualstudio.code'.format(HOME)
VSCODE_FLATPAK_DATA_ARCHIVE = '{0}/VSCodeFlatpakBackup'.format(BACKUP)
backup_folder(VSCODE_FLATPAK_DATA_ARCHIVE, VSCODE_FLATPAK_DATA_FOLDER)

# Backup Visual Studio Code (Extensions).
VSCODE_EXTENSIONS_FOLDER = '{0}/.vscode'.format(HOME)
VSCODE_EXTENSIONS_ARCHIVE = '{0}/VSCodeExtensions'.format(BACKUP)
backup_folder(VSCODE_EXTENSIONS_ARCHIVE, VSCODE_EXTENSIONS_FOLDER)

# Backup Visual Studio Code (Configuration).
VSCODE_CONFIGURATION_FOLDER = '{0}/.config/Code'.format(HOME)
VSCODE_CONFIGURATION_ARCHIVE = '{0}/VSCodeConfiguration'.format(BACKUP)
backup_folder(VSCODE_CONFIGURATION_ARCHIVE, VSCODE_CONFIGURATION_FOLDER)

# Backup VLC (Flatpak).
VLC_FLATPAK_DATA_FOLDER = '{0}/.var/app/org.videolan.VLC'.format(HOME)
VLC_FLATPAK_DATA_ARCHIVE = '{0}/VLCFlatpakBackup'.format(BACKUP)
backup_folder(VLC_FLATPAK_DATA_ARCHIVE, VLC_FLATPAK_DATA_FOLDER)

# Backup Workspace.
DOCUMENTS_DATA_FOLDER = '{0}/Documents/Workspace'.format(HOME)
DOCUMENTS_DATA_ARCHIVE = '{0}/WorkspaceBackup'.format(BACKUP)
backup_folder(DOCUMENTS_DATA_ARCHIVE, DOCUMENTS_DATA_FOLDER)

create_checksum()

# Final newline.
sys.exit("\n{0}Files have been backed up to {1}.{2}\n".format(LIGHT_GREEN, BACKUP, COLOUR_RESET))

# End of File.
