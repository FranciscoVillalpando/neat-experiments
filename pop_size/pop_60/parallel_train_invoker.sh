#!/bin/bash


# Ordered by table in paper
GAME_0=("SonicAndKnuckles3-Genesis" "AngelIslandZone.Act1.state")
GAME_1=("SonicTheHedgehog2-Genesis" "AquaticRuinZone.Act1.state")
GAME_2=("SonicTheHedgehog2-Genesis" "AquaticRuinZone.Act2.state")
GAME_3=("SonicAndKnuckles3-Genesis" "CarnivalNightZone.Act1.state")
GAME_4=("SonicAndKnuckles3-Genesis" "CarnivalNightZone.Act2.state")
GAME_5=("SonicTheHedgehog2-Genesis" "CasinoNightZone.Act1.state")
GAME_6=("SonicTheHedgehog2-Genesis" "ChemicalPlantZone.Act1.state")
GAME_7=("SonicTheHedgehog2-Genesis" "ChemicalPlantZone.Act2.state")
GAME_8=("SonicAndKnuckles3-Genesis" "DeathEggZone.Act1.state")
GAME_9=("SonicAndKnuckles3-Genesis" "DeathEggZone.Act2.state")
GAME_10=("SonicTheHedgehog2-Genesis" "EmeraldHillZone.Act1.state")
GAME_11=("SonicTheHedgehog2-Genesis" "EmeraldHillZone.Act2.state")
GAME_12=("SonicAndKnuckles3-Genesis" "FlyingBatteryZone.Act1.state")
GAME_13=("SonicTheHedgehog-Genesis" "GreenHillZone.Act1.state")
GAME_14=("SonicTheHedgehog-Genesis" "GreenHillZone.Act3.state")
GAME_15=("SonicAndKnuckles3-Genesis" "HiddenPalaceZone.state")
GAME_16=("SonicTheHedgehog2-Genesis" "HillTopZone.Act1.state")
GAME_17=("SonicAndKnuckles3-Genesis" "HydrocityZone.Act2.state")
GAME_18=("SonicAndKnuckles3-Genesis" "IcecapZone.Act1.state")
GAME_19=("SonicAndKnuckles3-Genesis" "IcecapZone.Act2.state")
GAME_20=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act1.state")
GAME_21=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act2.state")
GAME_22=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act3.state")
GAME_23=("SonicAndKnuckles3-Genesis" "LaunchBaseZone.Act1.state")
GAME_24=("SonicAndKnuckles3-Genesis" "LaunchBaseZone.Act2.state")
GAME_25=("SonicAndKnuckles3-Genesis" "LavaReefZone.Act2.state")
GAME_26=("SonicAndKnuckles3-Genesis" "MarbleGardenZone.Act1.state")
GAME_27=("SonicAndKnuckles3-Genesis" "MarbleGardenZone.Act2.state")
GAME_28=("SonicTheHedgehog-Genesis" "MarbleZone.Act1.state")
GAME_29=("SonicTheHedgehog-Genesis" "MarbleZone.Act2.state")
GAME_30=("SonicTheHedgehog-Genesis" "MarbleZone.Act3.state")
GAME_31=("SonicTheHedgehog2-Genesis" "MetropolisZone.Act1.state")
GAME_32=("SonicTheHedgehog2-Genesis" "MetropolisZone.Act2.state")
GAME_33=("SonicAndKnuckles3-Genesis" "MushroomHillZone.Act1.state")
GAME_34=("SonicAndKnuckles3-Genesis" "MushroomHillZone.Act2.state")
GAME_35=("SonicTheHedgehog2-Genesis" "MysticCaveZone.Act1.state")
GAME_36=("SonicTheHedgehog2-Genesis" "MysticCaveZone.Act2.state")
GAME_37=("SonicTheHedgehog2-Genesis" "OilOceanZone.Act1.state")
GAME_38=("SonicTheHedgehog2-Genesis" "OilOceanZone.Act2.state")
GAME_39=("SonicAndKnuckles3-Genesis" "SandopolisZone.Act1.state")
GAME_40=("SonicAndKnuckles3-Genesis" "SandopolisZone.Act2.state")
GAME_41=("SonicTheHedgehog-Genesis" "ScrapBrainZone.Act2.state")
GAME_42=("SonicTheHedgehog-Genesis" "SpringYardZone.Act2.state")
GAME_43=("SonicTheHedgehog-Genesis" "SpringYardZone.Act3.state")
GAME_44=("SonicTheHedgehog-Genesis" "StarLightZone.Act1.state")
GAME_45=("SonicTheHedgehog-Genesis" "StarLightZone.Act2.state")
GAME_46=("SonicTheHedgehog2-Genesis" "WingFortressZone.state")

GAME_ARRAY=(
	GAME_13[@]
	GAME_13[@]
	GAME_13[@]
	GAME_13[@]
	GAME_13[@]
)

COUNT=${#GAME_ARRAY[@]}

timestamp= $(date +%s)

echo "Starting invoker script..."
echo "Starting run with ID: ${timestamp} "
echo "echo 'starting parallel jobs!'" > jobs
for ((i=0; i<$COUNT; i++))
do

    mkdir -p ./run_logs/run$i

	GAME=${!GAME_ARRAY[i]:0:1}
	LEVEL=${!GAME_ARRAY[i]:1:1}
	echo "python3 retro-train.py run$i ${GAME} ${LEVEL} >> ./run_logs/$timestamp/${LEVEL}_train_run${i}.txt" >> jobs

done

parallel --jobs 6 < jobs 

echo "Finishing invoker script..."
