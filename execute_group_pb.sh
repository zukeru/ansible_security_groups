
#!/usr/bin/env bash

PLAYBOOK=$1
ENV=groups/$2
echo "executing playbook"

if [ $PLAYBOOK == "all" ]; then
	groups=$(ls $ENV)
	for group in $groups; do
		ansible-playbook -i "localhost," -c local $ENV/$group
	done
else
	ansible-playbook -i "localhost," -c local $ENV/$PLAYBOOK
fi