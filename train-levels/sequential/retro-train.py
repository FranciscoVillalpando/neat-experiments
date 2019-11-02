import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime
import sys
import os
import glob
from neat.reporting import ReporterSet

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
        timestepCount += 1
        if(done):
            break
        ob, rew, done, info = env.step(nnOutput)
        fitness_current += rew
        timestepCount += 1
        if(done):
            break
        ob, rew, done, info = env.step(nnOutput)
        fitness_current += rew 
        timestepCount += 1
        if(done):
            break

        #if timestepCount >= timestepMax :
        #    print("Finished timestepMax at time: " + str(datetime.datetime.now()))
        #    exit(0)
        if fitness_current > current_max_fitness:
            current_max_fitness = fitness_current
            counter = 0
        else:
            counter += 1
            
        if done or counter == 110:
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
                
# Gets a map of genomes from a list of files
def get_genomes_from_files(files):

    print(f"Genome files = {files}")
    genome_map = {}
    for idx, file_name in enumerate(files):
        with open(file_name, 'rb') as genomefile:
            genome = pickle.load(genomefile)
            genome_map[genome.key]  = genome
            # genome.key = idx+1 # override key, failing to do so results in error at runtime
            # genome_map[idx+1] = genome

    return genome_map

if __name__ == "__main__":
    configfile = 'config.txt'
    max_generations = 150

    print("Starting python script!")

    print(f"Parameters: {sys.argv}")
    # If we have a file name argument use it as the file prefix
    game_name = ""
    state_name= ""
    run_name = ""
    init_pop = ""
    if len(sys.argv) > 4:
        run_name = sys.argv[1]
        game_name = sys.argv[2]
        state_name = sys.argv[3]
        init_pop = sys.argv[4:]
    elif len(sys.argv) > 3:
        run_name = sys.argv[1]
        game_name = sys.argv[2]
        state_name = sys.argv[3]
    elif len(sys.argv) > 1:
        run_name = sys.argv[1]
        game_name = 'SonicTheHedgehog-Genesis'
        state_name =  'GreenHillZone.Act1.state'
    else:
        run_name = 'runX'
        game_name = 'SonicTheHedgehog-Genesis'
        state_name =  'GreenHillZone.Act1.state'

    file_prefix = state_name + "_" + run_name

    print ("Using env(" + game_name + ", " + state_name + ")")

    env = retro.make(game_name, state_name, scenario="contest")
    iny, inx, inc = env.observation_space.shape
    print("Observation space shape:" + str(env.observation_space.shape))
    print("Using init pop files: {}".format(init_pop))

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

    p = None

    if(init_pop != ""):

        initial_population = get_genomes_from_files(init_pop)

        print(f"Working with initial population: {initial_population}")

        init_species = config.species_set_type(config.species_set_config, ReporterSet())
        init_species.speciate(config, initial_population, 0)

        initial_state = (initial_population, init_species, 0)
        
        p = neat.Population(config, initial_state)

    else:
        p = neat.Population(config)

    # Reporters and loggers
    p.add_reporter(neat.StdOutReporter(True))

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