#!/bin/bash
#==============================================================================
#title           :alterados.sh
#description     :This script will separate the files in X commits on another directory
#author		     :<Sérgio Berlotto Jr> sergio.berlotto@gmail.com
#date            :20121122
#version         :0.1
#usage		 	 :./alterados.sh <number_of_commits>
#note            :Use this script in your git repository directory
#bash_version    :4.2.36(1)
#licence         :GPLv3
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================

echo ==\>Copying modified files in $1 commits ...
d="/tmp/`date +%j%H%M%S`/"
echo ==\>Destiny: $d
mkdir $d

for f in `git whatchanged -n $1 | grep ^: | cut -d " " -f 5 | cut -f 2 | uniq`; do
	echo Arquivo $f
	dn=$(dirname $f) #dirname
	fn=$(basename $f) #filename
	nn=$d$dn #newname
	mkdir -p $nn
	cp $f $nn
	echo $nn
done

git log -n 9 --format='%h %ci - %cn (%ce)' > $d/release-commits.txt
echo ==\>List of alterations in: $d/release-commits.txt

echo Done!
