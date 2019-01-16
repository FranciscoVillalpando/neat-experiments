import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime

env = retro.make('AirStriker-Genesis', 'level1')
configfile = 'config-feedforward.txt'
max_generations = 200
print("Starting python script!")
print("Observation space shape:" + str( env.observation_space.shape))

print( "Start: " + str(datetime.datetime.now()))

inx, iny, inc = env.observation_space.shape

inx = int(inx/8)
iny = int(iny/8)
# Print config file
print("Using the following config file: " + configfile)
f = open(configfile,'r') 
print(f.read()) 
print("End of config file")

imgarray = []

#cv2.namedWindow("main", cv2.WINDOW_NORMAL)

def eval_genomes(genomes, config):

    for genome_id, genome in genomes:

        print( "New genome at : " + str(datetime.datetime.now()))

        ob = env.reset()

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        current_max_fitness = 0
        fitness_current = 0
        counter = 0
        
        done = False

        while not done:
            
            #env.render()
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = cv2.resize(ob, (inx, iny))
            #ob = np.reshape(ob, (iny,inx))

            #cv2.imshow('main',ob)

            imgarray = np.ndarray.flatten(ob)
            imgarray = np.append(imgarray,1)

            nnOutput = net.activate(imgarray)
            
            ob, rew, done, info = env.step(nnOutput)
                    
            fitness_current += rew
            
            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1
                
            if done or counter == 300:
                done = True
                print(genome_id, fitness_current)
                
            genome.fitness = fitness_current

                
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(2))

winner = p.run(eval_genomes, max_generations)

print("Winner!" + str(winner))

print( "End: " + str(datetime.datetime.now()))


with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
    

