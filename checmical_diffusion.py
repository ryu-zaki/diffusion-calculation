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

# Simulation loop
for t in range(1, num_rows):
    ppm_matrix[t, :] = ppm_matrix[t - 1, :]
    
    for i in range(1, num_cols - 1):
                                                                                      
        diffusion = diffusion_rate * (ppm_matrix[t-1, i-1] - 2 * ppm_matrix[t-1, i] + ppm_matrix[t-1, i+1])
        
        ppm_matrix[t, i] = ppm_matrix[t-1, i] + diffusion

print(ppm_matrix)