# This is an implementation of the famous frozen lake problem
import random

class Action_space:
    def __init__(self, actions):
        self.space = actions

    def sample(self):
        return self.space[random.randint(0,len(self.space)-1)]



class FrozenLake:
    def __init__(self, dim=4, slippery = 0.2):
        # this is where we are in the lake as x and y co-ordinates
        # For now we always start in the top left.
        self.posx = 0
        self.posy = 0
        # How big is the lake, default is 4x4
        self.dimension = dim
        # This is the set of actions we are allowed to take
        self.action_space = Action_space(('left', 'up', 'right', 'down'))
        # probability of 'slipping' i.e. a different direction to the one suggested will be used
        self.probSlip = slippery
        self.done = False
        # Where are the holes (hard coded for now)
        self.holes = ((3,1),(3,2),(0,3))

    def reset(self):
        self.posx = 0
        self.posy = 0
        self.done = False

    # return the current state
    def currentState(self):
        return self.posx, self.posy

    # At the moment the goal is always in the bottom left corner
    def reachedGoal(self):
        if (self.posx == (self.dimension -1)) and (self.posy == (self.dimension -1)):
            return True
        else:
            return False

    def inHole(self):
        if (self.posx, self.posy) in self.holes:
            return True
        else:
            return False


    # In this function we calculate what will happen if we take a step
    # We will update the internal state and decide if the epsiode is over
    # and what reward to return.
    def step(self, action):
        reward = 0
        if action in self.action_space.space: # Check the action is allowed.
            v = random.uniform(0,1)
            if v<=self.probSlip:
                action = self.action_space.sample()
            elif action == 'left':
                self.posx = max(0, self.posx-1)
            elif action == 'right':
                self.posx = min((self.dimension -1), self.posx + 1)
            elif action == 'up':
                self.posy = max(0, self.posy - 1)
            else:
                self.posy = min((self.dimension - 1), self.posy + 1)

            # now check where we are
            if self.inHole():
                reward = -10
                self.done = True
            elif self.reachedGoal():
                reward = +10
                self.done = True

        else:
            print('Err FrozenLake: No such action {} in call to step')
        return action, reward, self.done


def main():
    env = FrozenLake()
    env.reset()
    print ('Dimension = ', env.dimension)

    for i in range(10):
        action_pre = env.action_space.sample()
        action, reward, done = env.step(action_pre)
        # For diagnostics retrieve the state
        state = env.currentState()
        print('Tried : ',action_pre, ' executed : ',action, '. State is : ', state, 'Reward is :', reward, ' Done is :', done)
if __name__ == "__main__":
    main()