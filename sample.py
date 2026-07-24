import numpy as np

arr = range(1,5)
num_rows = 5
num_cols = 5

ppm_matrix = np.zeros((num_rows, num_cols))

initial_ppm = np.array([80.0, 0.0, 0.0, 0.0, 0.0])
ppm_matrix[0, :] = initial_ppm

for t in range(1, num_rows):
     ppm_matrix[t, :] = ppm_matrix[t - 1, :]
      
for i in range(1, num_cols - 1):
    print(i)

#print(ppm_matrix)