#!/bin/bash

if [ "$1" == "" ]; then
	echo "Need train run id..."
	exit 1
fi

if [ "$2" == "" ]; then
	echo "Need train run path..."
	exit 1
fi

echo "Starting invoker script..."
echo "Using $2 as initial population with ID $1"

# Ordered by table in paper
GAME_0=("SonicTheHedgehog-Genesis" "SpringYardZone.Act1.state")
GAME_1=("SonicTheHedgehog-Genesis" "GreenHillZone.Act2.state")
GAME_2=("SonicTheHedgehog-Genesis" "StarLightZone.Act3.state")
GAME_3=("SonicTheHedgehog-Genesis" "ScrapBrainZone.Act1.state")

GAME_4=("SonicTheHedgehog2-Genesis" "MetropolisZone.Act3.state")
GAME_5=("SonicTheHedgehog2-Genesis" "HillTopZone.Act2.state")
GAME_6=("SonicTheHedgehog2-Genesis" "CasinoNightZone.Act2.state")

GAME_7=("SonicAndKnuckles3-Genesis" "LavaReefZone.Act1.state")
GAME_8=("SonicAndKnuckles3-Genesis" "FlyingBatteryZone.Act2.state")
GAME_9=("SonicAndKnuckles3-Genesis" "HydrocityZone.Act1.state")
GAME_10=("SonicAndKnuckles3-Genesis" "AngelIslandZone.Act2.state")

GAME_ARRAY=(
  	GAME_0[@]
  	GAME_1[@]
  	GAME_2[@]
	GAME_3[@]
	GAME_4[@]
	GAME_5[@]
	GAME_6[@]
	GAME_7[@]
	GAME_8[@]
	GAME_9[@]
	GAME_10[@]
)
COUNT=${#GAME_ARRAY[@]}

echo "Starting run with ID: $1 "
echo "echo 'starting parallel jobs!'" > jobs
mkdir -p ./run_logs/$1
for ((i=0; i<$COUNT; i++))
do
	GAME=${!GAME_ARRAY[i]:0:1}
	LEVEL=${!GAME_ARRAY[i]:1:1}
	echo "python3 retro-test.py $1 ${GAME} ${LEVEL} $2 &> ./run_logs/$1/${LEVEL}_$1.txt" >> jobs

done

parallel --jobs 6 < jobs 

echo "Finishing invoker script..."
