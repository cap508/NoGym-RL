import random
from FrozenLake import FrozenLake as FL

env = FL()
env.reset()


alpha = 0.4
gamma = 0.999
epsilon = 0.017

# For diagnostics
actions = ('left', 'right', 'up', 'down')

# Step 1. initialize q
q = {}
for s in range(env.observation_space()):
    for a in range(env.action_space.n):
        q[(s,a)] = random.uniform(0,0.1)#0.0

def update_q_table(prev_state, action, reward, next_state, alpha, gamma):
    qa = max([q[(next_state,a)] for a in range(env.action_space.n)])
    q[(prev_state, action)] += alpha * (reward + gamma * qa - q[(prev_state, action)])

def epsilon_greedy_policy(state, epsilon):
    if random.uniform(0,1) < epsilon:
        return env.action_space.sample()
    else:
        return max(list(range(env.action_space.n)), key = lambda x: q[(state, x)])



# A support function to render the policy
def viewPolicy(env, q):
    for s in range(env.observation_space()):  # need to get FrozenLake to return observation_space and overvation_space.n
        a =  max(list(range(env.action_space.n)), key=lambda x: q[(s, x)])

        #We need to unpack this into something we can understand
        print ("policy : ",env.state2Tuple(s), actions[a])




# For each episode
for i in range(1000):
    r = 0

    print("--- Episode {} ---".format(i))
    prev_state = env.reset()
    while True:
        action = epsilon_greedy_policy(prev_state, epsilon)
        next_state, reward, done, action_done = env.step(action)
        print('Tried : ',actions[action], ' executed : ',actions[action_done], ' State is : ', env.state2Tuple(next_state), 'Reward is :', reward, ' Done is :', done)

        update_q_table(prev_state, action, reward, next_state, alpha, gamma)
        prev_state = next_state

        r += reward
        if done:
            break
    print("total reward : ", r)

viewPolicy(env, q)

print ('--- Q ---')
for v in q:
    print(env.state2Tuple(v[0]),actions[v[1]], q[v])