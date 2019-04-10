import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime
from sonic_util import SonicDiscretizer

path = 'experiment3'

configfile = './' +path+ '/config.txt'

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

env = retro.make('SonicAndKnuckles3-Genesis', 'HydrocityZone.Act1.state', scenario="contest")
env = SonicDiscretizer(env)
iny, inx, inc = env.observation_space.shape
inx = int(inx/2)
iny = int(iny/2)
genome = None
with open('./'+path+'/genomes/best_genome_run1_HydrocityZone.Act1.state_gen34.pkl', 'rb') as genomefile:
    genome = pickle.load(genomefile)

if genome is None :
    print('picke not found')
    exit()

net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

ob = env.reset()
done = False
fitness_current = 0
timestepCount = 0
current_max_fitness = 0
while not done:
            
    env.render()

    ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
    ob = cv2.resize(ob, (inx, iny))
    imgarray = np.ndarray.flatten(ob)

    nnOutput = net.activate(imgarray)

    ob, rew, done, info = env.step(nnOutput)
    fitness_current += rew


    timestepCount += 3

    if fitness_current > current_max_fitness:
            current_max_fitness = fitness_current

    #print(info)
    print(timestepCount,fitness_current)
