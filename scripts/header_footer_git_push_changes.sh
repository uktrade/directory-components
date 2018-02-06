#!/bin/bash
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
GREEN="\033[32m"
IFS= read -r -p "$(echo -e $BOLD$BLUE"Enter commit message: "$RESET)" commitmsg
IFS= read -r -p "$(echo -e $BOLD$BLUE"Enter JIRA ticket number (e.g. ED-1234): "$RESET)" ticketnum
for dir in $REPOS; do
  echo -e $BOLD$MAGENTA"Switching to repo $dir"$RESET
	cd $dir
	git add -A
	git commit -m "$commitmsg"
	git push -u origin $(git rev-parse --abbrev-ref HEAD)
	git pull-request -b master -m "$(printf "$(git rev-parse --abbrev-ref HEAD)\n\nhttps://uktrade.atlassian.net/browse/$ticketnum")"
done
