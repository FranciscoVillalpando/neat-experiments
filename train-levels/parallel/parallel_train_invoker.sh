#!/bin/bash


# Ordered by ocurrence in games

GAME_0=("SonicTheHedgehog-Genesis" "GreenHillZone.Act1.state")
GAME_1=("SonicTheHedgehog-Genesis" "GreenHillZone.Act3.state")
GAME_2=("SonicTheHedgehog-Genesis" "MarbleZone.Act1.state")
GAME_3=("SonicTheHedgehog-Genesis" "MarbleZone.Act2.state")
GAME_4=("SonicTheHedgehog-Genesis" "MarbleZone.Act3.state")
GAME_5=("SonicTheHedgehog-Genesis" "SpringYardZone.Act2.state")
GAME_6=("SonicTheHedgehog-Genesis" "SpringYardZone.Act3.state")
GAME_7=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act1.state")
GAME_8=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act2.state")
GAME_9=("SonicTheHedgehog-Genesis" "LabyrinthZone.Act3.state")
GAME_10=("SonicTheHedgehog-Genesis" "StarLightZone.Act1.state")
GAME_11=("SonicTheHedgehog-Genesis" "StarLightZone.Act2.state")
GAME_12=("SonicTheHedgehog-Genesis" "ScrapBrainZone.Act2.state")

GAME_13=("SonicTheHedgehog2-Genesis" "EmeraldHillZone.Act1.state")
GAME_14=("SonicTheHedgehog2-Genesis" "EmeraldHillZone.Act2.state")
GAME_15=("SonicTheHedgehog2-Genesis" "ChemicalPlantZone.Act1.state")
GAME_16=("SonicTheHedgehog2-Genesis" "ChemicalPlantZone.Act2.state")
GAME_17=("SonicTheHedgehog2-Genesis" "AquaticRuinZone.Act1.state")
GAME_18=("SonicTheHedgehog2-Genesis" "AquaticRuinZone.Act2.state")
GAME_19=("SonicTheHedgehog2-Genesis" "CasinoNightZone.Act1.state")
GAME_20=("SonicTheHedgehog2-Genesis" "HillTopZone.Act1.state")
GAME_21=("SonicTheHedgehog2-Genesis" "MysticCaveZone.Act1.state")
GAME_22=("SonicTheHedgehog2-Genesis" "MysticCaveZone.Act2.state")
GAME_23=("SonicTheHedgehog2-Genesis" "OilOceanZone.Act1.state")
GAME_24=("SonicTheHedgehog2-Genesis" "OilOceanZone.Act2.state")
GAME_25=("SonicTheHedgehog2-Genesis" "MetropolisZone.Act1.state")
GAME_26=("SonicTheHedgehog2-Genesis" "MetropolisZone.Act2.state")
GAME_27=("SonicTheHedgehog2-Genesis" "WingFortressZone.state")

GAME_28=("SonicAndKnuckles3-Genesis" "AngelIslandZone.Act1.state")
GAME_29=("SonicAndKnuckles3-Genesis" "HydrocityZone.Act2.state")
GAME_30=("SonicAndKnuckles3-Genesis" "MarbleGardenZone.Act1.state")
GAME_31=("SonicAndKnuckles3-Genesis" "MarbleGardenZone.Act2.state")
GAME_32=("SonicAndKnuckles3-Genesis" "CarnivalNightZone.Act1.state")
GAME_33=("SonicAndKnuckles3-Genesis" "CarnivalNightZone.Act2.state")
GAME_34=("SonicAndKnuckles3-Genesis" "IcecapZone.Act1.state")
GAME_35=("SonicAndKnuckles3-Genesis" "IcecapZone.Act2.state")
GAME_36=("SonicAndKnuckles3-Genesis" "LaunchBaseZone.Act1.state")
GAME_37=("SonicAndKnuckles3-Genesis" "LaunchBaseZone.Act2.state")
GAME_38=("SonicAndKnuckles3-Genesis" "MushroomHillZone.Act1.state")
GAME_39=("SonicAndKnuckles3-Genesis" "MushroomHillZone.Act2.state")
GAME_40=("SonicAndKnuckles3-Genesis" "FlyingBatteryZone.Act1.state")
GAME_41=("SonicAndKnuckles3-Genesis" "SandopolisZone.Act1.state")
GAME_42=("SonicAndKnuckles3-Genesis" "SandopolisZone.Act2.state")
GAME_43=("SonicAndKnuckles3-Genesis" "LavaReefZone.Act2.state")
GAME_44=("SonicAndKnuckles3-Genesis" "HiddenPalaceZone.state")
GAME_45=("SonicAndKnuckles3-Genesis" "DeathEggZone.Act1.state")
GAME_46=("SonicAndKnuckles3-Genesis" "DeathEggZone.Act2.state")

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
	GAME_11[@]
	GAME_12[@]
	GAME_13[@]
	GAME_14[@]
	GAME_15[@]
	GAME_16[@]
	GAME_17[@]
	GAME_18[@]
	GAME_19[@]
	GAME_20[@]
	GAME_21[@]
	GAME_22[@]
	GAME_23[@]
	GAME_24[@]
	GAME_25[@]
	GAME_26[@]
	GAME_27[@]
	GAME_28[@]
	GAME_29[@]
	GAME_30[@]
	GAME_31[@]
	GAME_32[@]
	GAME_33[@]
	GAME_34[@]
	GAME_35[@]
	GAME_36[@]
	GAME_37[@]
	GAME_38[@]
	GAME_39[@]
	GAME_40[@]
	GAME_41[@]
	GAME_42[@]
	GAME_43[@]
	GAME_44[@]
	GAME_45[@]
	GAME_46[@]
)

COUNT=${#GAME_ARRAY[@]}

run_id=$(date +%s)

echo "Starting invoker script..."
echo "Starting run with ID: ${run_id} "
mkdir -p ./run_logs/$run_id

echo "echo 'Starting jobs!'" > jobs
for ((i=0; i<$COUNT; i++))
do
	GAME=${!GAME_ARRAY[i]:0:1}
	LEVEL=${!GAME_ARRAY[i]:1:1}
	echo "python3 retro-train.py $run_id ${GAME} ${LEVEL} > ./run_logs/$run_id/${LEVEL}_train_${run_id}.txt" >> jobs
done

parallel --jobs 6 < jobs 

echo "Finishing invoker script..."