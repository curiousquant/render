import numpy as np
import matplotlib.pyplot as plt
np.random.seed(123)

def gen_paths(X0, theta, mu, sigma, T, num_steps, num_sims):
    dt = float(T) / num_steps
    paths = np.zeros((num_steps + 1, num_sims), np.float64)
    paths[0,:] = X0
    for t in range(1, num_steps + 1):
        rand = np.random.standard_normal(num_sims)
        paths[t,:] = paths[t-1,:] * np.exp(-theta * dt) + (mu - (sigma ** 2) / (2 * theta)) * (1 - np.exp(-theta * dt)) + np.sqrt((1 - np.exp(-2 * theta * dt)) * (sigma ** 2) / (2 * theta)) * rand
        print(paths[t,:] )
    return paths

# parms = {
# 'X0' : .5,
# 'theta' : .5,
# 'mu' : .5,
# 'sigma' : .1,
# 'T':1,
# 'num_steps' : 10,
# 'num_sims':5
# }
# paths = gen_paths(**parms)