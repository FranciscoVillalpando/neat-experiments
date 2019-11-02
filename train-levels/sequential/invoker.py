import subprocess
import time
import glob
import os

game_arr = [
    ("SonicTheHedgehog-Genesis","GreenHillZone.Act1.state"),
    ("SonicTheHedgehog-Genesis","GreenHillZone.Act3.state"),
    ("SonicTheHedgehog-Genesis","MarbleZone.Act1.state"),
    ("SonicTheHedgehog-Genesis","MarbleZone.Act2.state"),
    ("SonicTheHedgehog-Genesis","MarbleZone.Act3.state"),
    ("SonicTheHedgehog-Genesis","SpringYardZone.Act2.state"),
    ("SonicTheHedgehog-Genesis","SpringYardZone.Act3.state"),
    ("SonicTheHedgehog-Genesis","LabyrinthZone.Act1.state"),
    ("SonicTheHedgehog-Genesis","LabyrinthZone.Act2.state"),
    ("SonicTheHedgehog-Genesis","LabyrinthZone.Act3.state"),
    ("SonicTheHedgehog-Genesis","StarLightZone.Act1.state"),
    ("SonicTheHedgehog-Genesis","StarLightZone.Act2.state"),
    ("SonicTheHedgehog-Genesis","ScrapBrainZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","EmeraldHillZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","EmeraldHillZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","ChemicalPlantZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","ChemicalPlantZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","AquaticRuinZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","AquaticRuinZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","CasinoNightZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","HillTopZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","MysticCaveZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","MysticCaveZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","OilOceanZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","OilOceanZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","MetropolisZone.Act1.state"),
    ("SonicTheHedgehog2-Genesis","MetropolisZone.Act2.state"),
    ("SonicTheHedgehog2-Genesis","WingFortressZone.state"),
    ("SonicAndKnuckles3-Genesis","AngelIslandZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","HydrocityZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","MarbleGardenZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","MarbleGardenZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","CarnivalNightZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","CarnivalNightZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","IcecapZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","IcecapZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","LaunchBaseZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","LaunchBaseZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","MushroomHillZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","MushroomHillZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","FlyingBatteryZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","SandopolisZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","SandopolisZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","LavaReefZone.Act2.state"),
    ("SonicAndKnuckles3-Genesis","HiddenPalaceZone.state"),
    ("SonicAndKnuckles3-Genesis","DeathEggZone.Act1.state"),
    ("SonicAndKnuckles3-Genesis","DeathEggZone.Act2.state")
]

#source_id = 1563752118 
id = int(time.time()* 1000)
def get_genomes_files(path):
    files = glob.glob(path)
    return files

for i in enumerate(game_arr):
    #print(level)

    level = game_arr[i]

    out_file_name = f"./run_logs/{id}/{level[1]}_train_{id}.txt"
    # Create folder structure if it does not exist
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
    f = open(out_file_name, "w")

    init_genomes = get_genomes_files(f"./last_gen_genomes/{id}/{game_arr[i-1][1]}*")
    genomes_string = " ".join(init_genomes)

    command =  f"python3 retro-train.py {id} {level[0]} {level[1]} {genomes_string}"

    print(f"Running command: {command}")
    process = subprocess.run(command.split(), stdout=f, stderr=f)

