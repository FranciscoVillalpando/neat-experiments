import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime
import sys
import os
from sonic_util import SonicDiscretizer

file_prefix = ""
env = None
inx = 0
iny = 0
last_gen_genomes = []

current_gen = 1
timestepCount = 0
timestepMax = int(1e6)

# Evaluates a single genome (agent)
def eval_genome(genome, config):
    global timestepCount
    ob = env.reset()
    net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

    current_max_fitness = 0
    fitness_current = 0
    counter = 0 # to count no. of steps without progress 

    done = False

    while not done:
        
        #env.render()

        ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
        ob = cv2.resize(ob, (inx, iny))

        #cv2.imshow('main', ob)
        #cv2.waitKey(1) 

        imgarray = np.ndarray.flatten(ob)
        nnOutput = net.activate(imgarray)
        
        ob, rew, done, info = env.step(nnOutput)
        fitness_current += rew
        ob, rew, done, info = env.step(nnOutput)
        fitness_current += rew
        ob, rew, done, info = env.step(nnOutput)
        fitness_current += rew 

        timestepCount += 3
        #if timestepCount >= timestepMax :
        #    print("Finished timestepMax at time: " + str(datetime.datetime.now()))
        #    exit(0)
        if fitness_current > current_max_fitness:
            current_max_fitness = fitness_current
            counter = 0
        else:
            counter += 1
            
        if done or counter == 150:
            done = True
            
    print(genome.key, fitness_current)     
    genome.fitness = fitness_current

#Called once per generation
def eval_genomes(genomes, config):
    global current_gen
    global file_prefix
    global timestepCount
    global last_gen_genomes 
    best_fitness = 0
    max_generations = 2

    print("Gen timestep at time: " + str(datetime.datetime.now()))

    # last gen genomes
    last_gen_genomes.clear()

    for genome_id, genome in genomes:

        last_gen_genomes.append(genome)

        eval_genome(genome, config)

        # Save this genome if it is the best individual of the generation
        if genome.fitness > best_fitness:
            best_fitness = genome.fitness
            print("achieved fitness: " + str(best_fitness) + " at timestep " + str(timestepCount) + " time: " + str(datetime.datetime.now()))
            genome_name = './best_genomes/'+file_prefix+'_gen'+str(current_gen)+'.pkl'
            save_genome(genome_name,genome)

        # Save all the genomes for the last gen
 
    # Increment generation couter
    current_gen += 1
    print("Total timesteps at end of gen: " + str(timestepCount))

def save_genome(filename, genome):
    # Create folder structure if it does not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    print("Saving genome to file " + str(filename))
    with open(filename, 'wb') as output:
        pickle.dump(genome, output, 1)
                
def run_game(run_name, configfile, game_name, state_name):
    global env
    global inx,iny
    global last_gen_genomes
    global file_prefix
    max_generations = 2

    print("Starting python script!")

    file_prefix = state_name + "_" + run_name

    print ("Using env(" + game_name + ", " + state_name + ")")

    env = retro.make(game_name, state_name, scenario="contest")
    env = SonicDiscretizer(env)
    iny, inx, inc = env.observation_space.shape
    print("Observation space shape:" + str(env.observation_space.shape))

    #Scale observation space
    inx = int(inx/2)
    iny = int(iny/2)

    print( "Start: " + str(datetime.datetime.now()))    
    # Print config file
    print("Using the following config file: " + configfile)
    f = open(configfile,'r') 
    print(f.read()) 
    print("End of config file")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

    p = neat.Population(config)

    # Reporters and loggers
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, max_generations)

    print("Winner!" + str(winner))
    print( "End: " + str(datetime.datetime.now()))

    print("Saving stats...")
    stats.save()

    print("Storing last generation genomes")
    i = 1
    last_gen_genomes.sort(key=lambda x: x.fitness, reverse=True)
    for genome in last_gen_genomes:
        print(str(i) + ' ' +str(genome.fitness))
        genome_name = './last_gen_genomes/'+run_name+'/'+state_name+'_'+str(i)+'.pkl'
        save_genome(genome_name,genome)
        i += 1

    with open('winner_'+file_prefix+'.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)

if __name__ == "__main__":

    configfile = 'config.txt'

    run_number = 1
    if len(sys.argv) > 1:
        run_number = int(sys.argv[1])

    game_state_list = [
        ("SonicAndKnuckles3-Genesis", "AngelIslandZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "AquaticRuinZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "AquaticRuinZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "CarnivalNightZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "CarnivalNightZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "CasinoNightZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "ChemicalPlantZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "ChemicalPlantZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "DeathEggZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "DeathEggZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "EmeraldHillZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "EmeraldHillZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "FlyingBatteryZone.Act1.state"),
        ("SonicTheHedgehog-Genesis", "GreenHillZone.Act1.state"),
        ("SonicTheHedgehog-Genesis", "GreenHillZone.Act3.state"),
        ("SonicTheHedgehog2-Genesis", "HiddenPalaceZone.state"),
        ("SonicTheHedgehog2-Genesis", "HillTopZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "HydrocityZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "IcecapZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "IcecapZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "LabyrinthZone.Act1.state"),
        ("SonicTheHedgehog-Genesis", "LabyrinthZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "LabyrinthZone.Act3.state"),
        ("SonicAndKnuckles3-Genesis", "LaunchBaseZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "LaunchBaseZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "LavaReefZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "MarbleGardenZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "MarbleGardenZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "MarbleZone.Act1.state"),
        ("SonicTheHedgehog-Genesis", "MarbleZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "MarbleZone.Act3.state"),
        ("SonicTheHedgehog2-Genesis", "MetropolisZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "MetropolisZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "MushroomHillZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "MushroomHillZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "MysticCaveZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "MysticCaveZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "OilOceanZone.Act1.state"),
        ("SonicTheHedgehog2-Genesis", "OilOceanZone.Act2.state"),
        ("SonicAndKnuckles3-Genesis", "SandopolisZone.Act1.state"),
        ("SonicAndKnuckles3-Genesis", "SandopolisZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "ScrapBrainZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "SpringYardZone.Act2.state"),
        ("SonicTheHedgehog-Genesis", "SpringYardZone.Act3.state"),
        ("SonicTheHedgehog-Genesis", "StarLightZone.Act1.state"),
        ("SonicTheHedgehog-Genesis", "StarLightZone.Act2.state"),
        ("SonicTheHedgehog2-Genesis", "WingFortressZone.state")
    ]
    
    for run in range(run_number):

        for game_state in game_state_list:
            game = game_state[0]
            state = game_state[1]
            run_game('run'+ str(run), configfile, game, state)
