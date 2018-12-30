#!/bin/bash

if [ "$1" == "" ]; then

	echo "Need No. runs..."

	exit 1

fi

echo "Starting invoker script..."
echo "Running $1 cycles"

#git clone https://github.com/FranciscoVillalpando/test2.git
#cd test2
#git status

for (( c=1; c<=$1; c++ ))
do  
	echo "===================================="
   	echo "Starting run $c "

  	./script.sh run$c.txt
done
 
#./script 

echo "Finishing invoker script..."
