import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime

env = retro.make('SonicTheHedgehog-Genesis', 'GreenHillZone.Act1.state')
configfile = 'config-feedforward.txt'
max_generations = 200
print("Starting python script!")


iny, inx, inc = env.observation_space.shape
inx = int(inx/8)
iny = int(iny/8)
print("Observation space shape:" + str( env.observation_space.shape))
print( "Start: " + str(datetime.datetime.now()))

# Print config file
print("Using the following config file: " + configfile)
f = open(configfile,'r') 
print(f.read()) 
print("End of config file")


current_gen = 0

#Called once per generation
def eval_genomes(genomes, config):
    global current_gen
    best_fitness = 0

    for genome_id, genome in genomes:

        ob = env.reset()
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        current_max_fitness = 0
        fitness_current = 0
        counter = 0 # to count no. of steps without progress 
        
        done = False

        while not done:
            
            #env.render()

            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = cv2.resize(ob, (inx, iny))
            #ob = np.reshape(ob, (iny, inx))

            #cv2.imshow('main', ob)
            #cv2.waitKey(1) 

            imgarray = np.ndarray.flatten(ob)
            imgarray = np.append(imgarray, 1) # Input Layer bias?

            nnOutput = net.activate(imgarray)
            
            ob, rew, done, info = env.step(nnOutput)
            fitness_current += info['x'] - fitness_current

            ob, rew, done, info = env.step(nnOutput)
            fitness_current += info['x'] - fitness_current

            ob, rew, done, info = env.step(nnOutput)
            fitness_current += info['x'] - fitness_current
        
            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1
                
            if done or counter == 100:
                done = True
                print(genome_id, fitness_current)
                
            genome.fitness = current_max_fitness

        # Save this genome if it is the best individual of the generation
        if genome.fitness > best_fitness:
            best_fitness = genome.fitness
            save_genome('best_genome_gen'+str(current_gen)+'_'+str(genome_id)+'.pkl',genome)

    # Increment generation couter
    current_gen += 1

def save_genome(filename, genome):
    print("Saving genome to file " + str(filename))
    with open(filename, 'wb') as output:
        pickle.dump(genome, output, 1)
                
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(3)) # Create a checkpoint every n generations

winner = p.run(eval_genomes, max_generations)

print("Winner!" + str(winner))
print( "End: " + str(datetime.datetime.now()))

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
    

