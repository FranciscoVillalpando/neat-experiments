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
#env = retro.make('SonicTheHedgehog-Genesis', 'GreenHillZone.Act1.state')
#env = make_env(stack=False, scale_rew=False)
env = None
inx = 0
iny = 0

current_gen = 0
timestepCount = 0
timestepMax = int(1e6)

#Called once per generation
def eval_genomes(genomes, config):
    global current_gen
    global file_prefix
    global timestepCount
    best_fitness = 0
    print("Gen timestep at time: " + str(datetime.datetime.now()))

    for genome_id, genome in genomes:

        ob = env.reset()
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        current_max_fitness = 0
        fitness_current = 0
        counter = 0 # to count no. of steps without progress 
        
        done = False

        while not done:
            
            env.render()

            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = cv2.resize(ob, (inx, iny))
            #ob = np.reshape(ob, (iny, inx))

            #cv2.imshow('main', ob)
            #cv2.waitKey(1) 

            imgarray = np.ndarray.flatten(ob)
            #imgarray = np.append(imgarray, 1) # Input Layer bias?

            nnOutput = net.activate(imgarray)
            
            #env.step(nnOutput)
            #env.step(nnOutput)
            ob, rew, done, info = env.step(nnOutput)
            if rew != 0:
                print("rew: " + str(rew))
            fitness_current = info['x']

            timestepCount += 3

            if timestepCount >= timestepMax :
                print("Finished timestepMax at time: " + str(datetime.datetime.now()))
                exit(0)
            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1
                
            if done or info['lives'] < 3 or counter == 100:
                done = True
                print(genome_id, current_max_fitness)
                
        genome.fitness = current_max_fitness

        # Save this genome if it is the best individual of the generation
        if genome.fitness > best_fitness:
            best_fitness = genome.fitness
            print("achieved fitness: " + str(best_fitness) + " at timestep " + str(timestepCount) + " time: " + str(datetime.datetime.now()))
            genome_name = './genomes/best_genome_'+file_prefix+'_gen'+str(current_gen)
            save_genome(genome_name+'.pkl',genome)

    # Increment generation couter
    current_gen += 1
    print("Total timesteps at end of gen: " + str(timestepCount))

def save_genome(filename, genome):

    # Create folder structure if it does not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    print("Saving genome to file " + str(filename))
    with open(filename, 'wb') as output:
        pickle.dump(genome, output, 1)
                
if __name__ == "__main__":
    configfile = 'config.txt'
    max_generations = 500
    #global inx, iny, env


    print("Starting python script!")

    # If we have a file name argument use it as the file prefix
    if len(sys.argv) > 1:
        file_prefix = sys.argv[1]

    # If we have a file name argument use it as the file prefix
    if len(sys.argv) > 3:
        game_name = sys.argv[2]
        state_name = sys.argv[3]
        file_prefix += "_" + state_name
    else:
        game_name = 'SonicTheHedgehog-Genesis'
        state_name =  'GreenHillZone.Act1.state'

    print ("Using env(" + game_name + ", " + state_name + ")")

    env = retro.make(game_name, state_name)
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
    p.add_reporter(neat.Checkpointer(5)) # Create a checkpoint every n generations

    winner = p.run(eval_genomes, max_generations)

    print("Winner!" + str(winner))
    print( "End: " + str(datetime.datetime.now()))

    print("Saving stats...")
    stats.save()

    # print("Visualizing stats...")

    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    with open('winner_'+file_prefix+'.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)