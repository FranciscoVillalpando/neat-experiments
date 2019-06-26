import retro
import numpy as np
import cv2 
import neat
import pickle
import datetime

path = 'experiment1'

configfile = './' +path+ '/config.txt'

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     configfile)

env = retro.make('SonicTheHedgehog-Genesis', 'GreenHillZone.Act2.state')
iny, inx, inc = env.observation_space.shape
inx = int(inx/8)
iny = int(iny/8)
genome = None
with open('./'+path+'/.pkl', 'rb') as genomefile:
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
    imgarray = np.append(imgarray, 1) # Input Layer bias?

    nnOutput = net.activate(imgarray)

    ob, rew, done, info = env.step(nnOutput)
    fitness_current += info['x'] - fitness_current
    ob, rew, done, info = env.step(nnOutput)
    fitness_current += info['x'] - fitness_current
    ob, rew, done, info = env.step(nnOutput)
    fitness_current += info['x'] - fitness_current

    print(info)
    print(fitness_current)
