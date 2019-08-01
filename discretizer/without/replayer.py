import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime
import time

path = '.'

configfile = './' +path+ '/config_train.txt'

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

env = retro.make('SonicTheHedgehog-Genesis', 'GreenHillZone.Act1.state', scenario="contest")
iny, inx, inc = env.observation_space.shape
inx = int(inx/2)
iny = int(iny/2)
genome = None
with open('./best_genomes/GreenHillZone.Act1.state_run0_gen18.pkl', 'rb') as genomefile:
    genome = pickle.load(genomefile)

if genome is None :
    print('picke not found')
    exit()

net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

ob = env.reset()
done = False
fitness_current = 0
while not done:
            
    env.render()

    ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
    ob = cv2.resize(ob, (inx, iny))
    imgarray = np.ndarray.flatten(ob)

    nnOutput = net.activate(imgarray)

    ob, rew, done, info = env.step(nnOutput)
    fitness_current += rew

    print(info)
    print("fitness_current: {}".format(fitness_current))
    
    ob, rew, done, info = env.step(nnOutput)
    fitness_current += rew
 
    print(info)
    print("fitness_current: {}".format(fitness_current))

    ob, rew, done, info = env.step(nnOutput)
    fitness_current += rew

    print(info)
    print("fitness_current: {}".format(fitness_current))

