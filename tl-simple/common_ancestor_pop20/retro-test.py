import retro
import numpy as np
import cv2 
import neat
from neat.reporting import ReporterSet
import pickle
import datetime
import sys
import os
import glob

file_prefix = ""
env = None
inx = 0
iny = 0
global_best_fitness = 0
current_gen = 1
timestepCount = 0
timestepMax = int(1e6)
best_genome_data = [0, (0,0)] # [Score, (Size1, Size2)]

# Evaluates a single genome (agent)
def eval_genome(genome, config):
    global timestepCount
    global global_best_fitness
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
        if timestepCount >= timestepMax :
            print("Finished timestepMax at time: " + str(datetime.datetime.now()))
            # Print Generation info one last time so we can track it when we extract stats
            print(f"Best fitness: {best_genome_data[0]} - size: {best_genome_data[1]} - species 1 - id {0}")
            exit(0)
            
    print(   "-- genome with id {} done, fitness: {}".format(genome.key, fitness_current))     
    genome.fitness = fitness_current

#Called once per generation
def eval_genomes(genomes, config):
    global current_gen
    global file_prefix
    global timestepCount
    global best_genome_data

    print("Gen timestep at time: " + str(datetime.datetime.now()))

    for genome_id, genome in genomes:

        eval_genome(genome, config)

        # Save this genome if it is the best individual of the generation
        if genome.fitness > best_genome_data[0]:
            best_genome_data[0] = genome.fitness
            best_genome_data[1] = genome.size()
            print("achieved fitness: {} at timestep {} time: {}".format(best_fitness,timestepCount,datetime.datetime.now()))
            genome_name = './best_genomes/'+file_prefix+'_gen'+str(current_gen)+'.pkl'
            save_genome(genome_name,genome)
 
    # Increment generation couter
    current_gen += 1
    print("Total timesteps at end of gen: " + str(timestepCount))

def save_genome(filename, genome):

    # Create folder structure if it does not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    print("Saving genome to file " + str(filename))
    with open(filename, 'wb') as output:
        pickle.dump(genome, output, 1)

# Get the file names of the top genomes for each state
# tries to get a uniform distribution accross states,
# the remaining requested files are taken at random.
def get_top_genomes_file_names(genome_path,pop_size):
    import random

    # There are 47 train levels, prioritize variety
    train_level_n = 47 
    top_to_get = int (pop_size / train_level_n)
    remaining_genomes = pop_size % train_level_n

    path = f"{genome_path}"
    
    # Get the topk genomes for every state
    file_name_list = []
    for i in range(1, top_to_get+1):
        idx_list = glob.glob(path + "*_"+str(i)+ ".pkl")
        file_name_list.extend(idx_list)

    # Get remaining genomes from random states
    idx_list = glob.glob(path + "*_"+str(top_to_get+1)+ ".pkl")

    idx_list = random.sample(idx_list, remaining_genomes)
    file_name_list.extend(idx_list)

    return file_name_list

# Gets a map of genomes from a list of files
def get_genomes_from_files(file_list):

    genome_map = {}
    for idx, file_name in enumerate(file_list):
        with open(file_name, 'rb') as genomefile:
            genome = pickle.load(genomefile)
            #genome.key = idx+1 # override key, failing to do so results in error at runtime
            genome_map[genome.key] = genome

    return genome_map

if __name__ == "__main__":
    configfile = 'config_test.txt'
    max_generations = 200

    print("Starting python script!")

    print(sys.argv)
    # If we have a file name argument use it as the file prefix
    game_name = ""
    state_name= ""
    run_id = ""
    initial_pop_path = ""
    if len(sys.argv) > 4:
        run_name = sys.argv[1]
        game_name = sys.argv[2]
        state_name = sys.argv[3]
        initial_pop_path = sys.argv[4]
    elif len(sys.argv) > 1:
        run_id = sys.argv[1]
        game_name = 'SonicTheHedgehog-Genesis'
        state_name =  'ScrapBrainZone.Act1.state'
    else:
        print("Need run ID")
        exit(1)

    file_prefix = "{}_{}".format(state_name,run_id)

    print ("Using env({},{})".format(game_name,state_name))

    env = retro.make(game_name, state_name, scenario="contest")
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

    #Override population with pretrained population
    genome_files = get_top_genomes_file_names(initial_pop_path,config.pop_size)
    print(genome_files)
    initial_population = get_genomes_from_files(genome_files)

    init_species = config.species_set_type(config.species_set_config, ReporterSet())
    init_species.speciate(config, initial_population, 0)

    initial_state = (initial_population, init_species, 0)
    p = neat.Population(config, initial_state)

    # Reporters and loggers
    p.add_reporter(neat.StdOutReporter(True))

    winner = p.run(eval_genomes, max_generations)

    print("Winner!" + str(winner))
    print( "End: " + str(datetime.datetime.now()))

    # Save winner genome
    save_genome('./winner_genomes/winner_{}.pkl'.format(file_prefix),winner)