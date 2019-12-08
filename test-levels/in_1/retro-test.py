import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime
import sys
import os

file_prefix = ""
env = None
inx = 0
iny = 0

current_gen = 0
timestepCount = 0
timestepMax = int(1e6)

# Evaluates a single genome (agent)
def eval_genome(genome, config):
    global timestepCount
    ob = env.reset()
    net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

    fitness_current = 0

    done = False

    while not done:
        
        #env.render()

        ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)

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
            exit(0)
            
    print(genome.key, fitness_current)     
    genome.fitness = fitness_current

#Called once per generation
def eval_genomes(genomes, config):
    global current_gen
    global file_prefix
    global timestepCount
    best_fitness = 0
    print("Gen timestep at time: " + str(datetime.datetime.now()))

    for genome_id, genome in genomes:

        eval_genome(genome, config)

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

    env = retro.make(game_name, state_name, scenario="contest")
    iny, inx, inc = env.observation_space.shape
    print("Observation space shape:" + str(env.observation_space.shape))

    #Scale observation space
    #inx = int(inx/2)
    #iny = int(iny/2)

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