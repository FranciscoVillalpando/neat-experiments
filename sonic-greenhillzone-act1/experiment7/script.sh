#!/bin/bash

if [ "$1" == "" ]; then

	echo "Need out name..."
	exit 1

fi

echo "Starting script..."
echo "Writing output to $1"

#git clone https://github.com/FranciscoVillalpando/test2.git
#cd test2
#git status
 
python3 retro-test.py >> $1

echo "Finishing script..."
