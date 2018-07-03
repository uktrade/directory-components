#!/bin/bash
set -e
REPOS="
../directory-sso
../directory-sso-profile
../help
../directory-ui-buyer
../directory-ui-export-readiness
../navigator"
BOLD="\033[1m"
RESET="\033[0m"
MAGENTA="\033[95m"
BLUE="\033[34m"
IFS= read -r -p "$(echo -e $BOLD$BLUE"Enter the name of the git branch to create followed by [ENTER]: "$RESET)" branch
for dir in $REPOS; do
	echo -e $BOLD$MAGENTA"Switching to repo $dir"$RESET
	cd $dir
	git stash
	git checkout master
	git pull
	git checkout -b $branch
done
