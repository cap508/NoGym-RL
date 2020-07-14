# This is an implementation of the famous frozen lake problem
import random

class Action_space:
    def __init__(self, actions):
        self.n = len(actions)
        self.space = actions

    def sample(self):
        return self.space[random.randint(0,len(self.space)-1)]



class FrozenLake:
    def __init__(self, dim=4, slippery = 0.2):
        # this is where we are in the lake as x and y co-ordinates
        # For now we always start in the top left.
        self.col = 0
        self.row = 0
        # How big is the lake, default is 4x4
        self.dimension = dim
        # This is the set of actions we are allowed to take
#        self.action_space = Action_space(('left', 'right', 'up', 'down'))
        self.action_space = Action_space((0, 1, 2, 3))
        # probability of 'slipping' i.e. a different direction to the one suggested will be used
        self.probSlip = slippery
        self.done = False
        # Where are the holes (hard coded for now)
        self.holes = ((1,3),(2,3),(3,0)) #(row, col)

    def reset(self):
        self.col = 0
        self.row = 0
        self.done = False
        return self.currentState()

    def observation_space(self):
        return self.dimension * self.dimension

    # return the current state
    def currentState(self):
        return self.row * self.dimension + self.col

    # support function for rendering states
    def state2Tuple(self, state):
        return (state // 4, state % 4) # (row, col)


    # At the moment the goal is always in the bottom left corner
    def reachedGoal(self):
        if (self.col == (self.dimension - 1)) and (self.row == (self.dimension - 1)):
            return True
        else:
            return False

    def inHole(self):
        if (self.row, self.col) in self.holes:
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

            if action == 0:#'left':
                self.col = max(0, self.col - 1)
            elif action == 1:#'right':
                self.col = min((self.dimension - 1), self.col + 1)
            elif action == 2:#'up':
                self.row = max(0, self.row - 1)
            else:
                self.row = min((self.dimension - 1), self.row + 1)

            # now check where we are
            if self.inHole():
                reward = -10
                self.done = True
            elif self.reachedGoal():
                reward = +10
                self.done = True

        else:
            print('Err FrozenLake: No such action {} in call to step')
        return self.currentState(), reward, self.done, action

    def render(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
                if (row == self.row) and (col == self.col):
                    print('X', end="")
                elif (row == 0 and col ==0):
                    print('S', end="")
                elif (row,col) in self.holes:
                    print('H', end="")
                elif (row == (self.dimension -1)) and (col == (self.dimension -1)):
                    print('G', end="")
                else:
                    print('.', end="")
            print('')


# Test the environment
def main():
    env = FrozenLake()
    env.reset()
    print ('Dimension = ', env.dimension)
    # For diagnostics
    actions = ('left', 'right', 'up', 'down')


#    for i in range(10):
    while env.done == False:
        env.render()
        action_pre = env.action_space.sample()
        state, reward, done, action = env.step(action_pre)
        print('Tried : ',actions[action_pre], ' executed : ',actions[action], '. State is : ', env.state2Tuple(state), 'Reward is :', reward, ' Done is :', done)

    env.render()

if __name__ == "__main__":
    main()