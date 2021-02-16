#!/usr/bin/env Rscript

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

#########
# Notes #
#########

# - This script works in conjunction with the shell script named
#   'bootstrap_bioinformatics_container.sh'.
# - Open and run this file using R Studio to install some useful data
#   science and bioinformatics libraries.
# - If you are using Anaconda/Miniconda, please disable your 'conda'
#   environment before running this script as it will interfere with
#   building R packages from source.

#############
# Variables #
#############

R_PACKAGES <- c(
  'arules',
  'arulesViz',
  'biclust',
  'BiocManager',
  'boot',
  'car',
  'caret',
  'class',
  'cluster',
  'codetools',
  'dplyr',
  'e1071',
  'forecast',
  'foreign',
  'GGally',
  'ggplot2',
  'gplots',
  'Hmisc',
  'igraph',
  'igraphdata',
  'kernlab',
  'KernSmooth',
  'kohonen',
  'learnr',
  'linkcomm',
  'lubridate',
  'MASS',
  'Matrix',
  'mctest',
  'missForest',
  'MVA',
  'neuralnet',
  'nlme',
  'nnet',
  'nycflights13',
  'randomForest',
  'rattle',
  'RColorBrewer',
  'ROCR',
  'rpart.plot',
  'rpart',
  'seqinr',
  'spatial',
  'tidyr',
  'tidyverse',
  'utils',
  'VIM'
)

#############
# Functions #
#############

install_bioc_pkgs <- function(){
  BiocManager::install(c("DESeq2", "biomaRt"))
}

#############
# Kickstart #
#############

install.packages(R_PACKAGES, dependencies=TRUE)

install_bioc_pkgs()

# End of File.
