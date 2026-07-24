import numpy as np

# Pipe parameters
pipe_length_m = 20.0
num_nodes = 5
space_grid = np.linspace(0.0, pipe_length_m, num_nodes) # [0, 5, 10, 15, 20]

# Time steps: 0s to 8s with 2s intervals -> [0, 2, 4, 6, 8]
time_steps = np.arange(0, 9, 2) 

num_rows = len(time_steps) # 5
num_cols = len(space_grid) # 5 
ppm_matrix = np.zeros((num_rows, num_cols)) # to create a table or matric (5 columns x 5 rows)

# Initial State at t = 0s
# Node 0 is 80 ppm, rest are 0 ppm
initial_ppm = np.array([80.0, 0.0, 0.0, 0.0, 0.0])
ppm_matrix[0, :] = initial_ppm

diffusion_rate = 0.20
