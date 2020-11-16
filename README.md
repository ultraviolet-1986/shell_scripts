# Shell Scripts

A collection of shell scripts in various languages.

## Table of Contents

- [BASH Scripts](#bash-scripts)
  - [automate_anaconda3_installation.sh](#automate_anaconda3_installation.sh)
  - [bootstrap_fedora_silverblue.sh](#bootstrap_fedora_silverblue.sh)
  - [bootstrap_fedora_workstation.sh](#bootstrap_fedora_workstation.sh)
  - [bootstrap_rstudio_container.sh](#bootstrap_rstudio_container.sh)
- [Python 3 Scripts](#python-3-scripts)
  - [pybackup.py](#pybackup.py)
  - [pygpg.py](#pygpg.py)
  - [pyiso.py](#pyiso.py)
  - [pyminecraft.py](#pyminecraft.py)
  - [pysetup.py](#pysetup.py)
  - [pysilverblue.py](#pysilverblue.py)
- [R scripts](#r-scripts)
  - [data_science_packages.R](#data_science_packages.R)

## BASH Scripts

### `automate_anaconda3_installation.sh`

This script will automatically download, verify, and install the
[Anaconda 3](https://tinyurl.com/yb6ozrnq) Python distribution with its default
settings. Note that the version installed may not be the newest, but they will
also be verified by `SHA-256` before being installed to verify that the
installation is safe and genuine. Take care to verify the `SHA-256` checksum
before executing this script.

### `bootstrap_fedora_silverblue.sh`

This script will help to build a functional Fedora Silverblue installation from
fresh, note that because of the atomic nature of this process, the user must
manually reboot the system, start the script again and select the next
consecutive option from the main menu.

### `bootstrap_fedora_workstation.sh`

This script will automatically configure a Fedora Workstation installation from
scratch. This script should be run as root to enable all operations to complete
without requiring further user authentication over time. It is
**very important** that the user read and understand all of the code contained
before running this script; it modifies system software and is intended to be
ran **only once**: when Fedora Workstation has been newly installed.

### `bootstrap_rstudio_container.sh`

This script uses [Toolbox](https://tinyurl.com/y4t5ezo7) to create a complete R
development environment separate from the main system. Running this script will
create a container named `rdev` which will be created, updated, and configured
with [R Studio](https://tinyurl.com/wkvl284) and package-building dependencies.
Note that is the user is also running the `Anaconda 3` Python distribution, it
can interfere with R source package building so the user should use the command
`conda deactivate` before running `R Studio` or building R packages from source.

It is possible to automate this process by inserting the following code within
your `.bashrc` file:

```bash
# Check user is using a Container. FOR BASHRC: PLACE AFTER CONDA.
if [ -v "$VARIANT_ID" ] && [ "$VARIANT_ID" == 'container' ] ; then
  conda deactivate
fi
```

Note that this code must be placed after the line reading:
`# <<< conda initialize <<<`. When the user opens a container within their
Terminal, the `.bashrc` file will determine whether the user is operating within
a container and deactivate `conda` until the container is closed by using the
`exit` command.

The container itself will be based on the current stable version of
[Fedora](https://tinyurl.com/obf34x5) (at the time of writing, this is Fedora
33). When the container has started, it is possible to run `R Studio` by using
the `rstudio` command. Note that the Terminal must be left open for this process
to work correctly.

Once the container has been successfully bootstrapped, it is possible to enter
the container by using the following command:

```bash
toolbox enter rdev
```

## Python 3 Scripts

### `pybackup.py`

This script will detect and archive settings folders for detected applications
currently installed to prevent the user from having to reconfigure in the event
they need to reinstall their Operating System. The user will have the option to
create the backup within their home folder as `$HOSTNAME_Backup`, or an external
storage device, providing the device has a label of `$HOSTNAME` in capital
letters. Replace `$HOSTNAME` with the name of your computer.

### `pygpg.py`

This script will allow the user to use GPG encryption to encrypt and decrypt a
given file with a password. The operation will depend on the user passing an
argument of `--encrypt` or `--decrypt` and the name of an existing file. This
script requires that the user has the package `gnupg2` installed (correct for
Fedora).

### `pyiso.py`

This script will create a mountable read-only ISO disk image of a given folder
and is useful for archiving purposes. Note that this disk image will be UDF
format and will also be non ISO-9660 compliant.

### `pyminecraft.py`

This script will download the latest version of the
[Minecraft: Java Edition](https://tinyurl.com/ssudojg) launcher and place it
within a mountable ISO disk image. This disk image will prompt the user to start
the launcher when mounted.

### `pysetup.py`

This script will help the user to maintain their Linux desktop by updating
system software and [ClamAV](https://tinyurl.com/y7v3zglf) virus definitions.
Note the default package manager will be detected and launched automatically,
most common package managers are supported, but may require user password.

### `pysilverblue.py`

This script allows the user to hot-swap some RPM software with their Flatpak
equivalents, and back again. This is to potentially resolve dependency issues
when updating software using RPM-OSTree.

## R scripts

### `data_science_packages.R`

This script will install some useful data science libraries and is intended to
be executed from `R Studio` in conjunction with the
`bootstrap_r_development_container.sh` script. If the process has been followed
correctly and `conda` is disabled (if installed), the building and installation
of these packages should complete without any failures.
