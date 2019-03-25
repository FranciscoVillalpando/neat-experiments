import retro
from sonic_util import SonicDiscretizer

game_name = 'SonicTheHedgehog-Genesis'
state_name =  'GreenHillZone.Act1.state'
env = retro.make(game_name, state_name)
env = SonicDiscretizer(env)
env.reset()
print('retro.Actions.DISCRETE action_space', env.action_space)

action  = [0,0,0,0,0,0,0]
action  = [0,0,0,0,0,0,0]
while (True):
    env.render()
    ob, rew, done, info = env.step(action)
    if rew != 0:
        print(rew)