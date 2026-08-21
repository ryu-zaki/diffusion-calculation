import numpy as np
# pyrefly: ignore [missing-import]
from scipy.spatial.distance import euclidean, cityblock
# pyrefly: ignore [missing-import]
from scipy.interpolate import interp1d

# Given Data
warehouse = [0, 0]
locations = [
    [2, 3],
    [4, 2],
    [5, 5],
    [7, 5],
    [8, 8]
]
fuel_consumed = np.array([0.6, 0.8, 1.2, 1.5, 2.0])

# Task 1 & 2: Compute Euclidean and Cityblock distances
euclidean_distances = []
cityblock_distances = []

for loc in locations:
    e_dist = euclidean(warehouse, loc)
    c_dist = cityblock(warehouse, loc)
    euclidean_distances.append(round(e_dist, 2)) # Rounded to 2 decimal places for cleaner output
    cityblock_distances.append(c_dist)

# Convert to numpy arrays for interpolation
euclidean_distances = np.array(euclidean_distances)
cityblock_distances = np.array(cityblock_distances)

# Task 3: Create linear interpolation function
# X = cityblock_distances, Y = fuel_consumed
fuel_estimator = interp1d(cityblock_distances, fuel_consumed, kind='linear')

# Task 4: Calculate for new location [6, 4]
new_location = [6, 4]
new_cityblock = cityblock(warehouse, new_location)
estimated_fuel = fuel_estimator(new_cityblock)

print(fuel_estimator)

# Expected Output Format
print(f"Euclidean Distances (km): {euclidean_distances.tolist()}")
print(f"Cityblock Distances (km): {cityblock_distances.tolist()}")
print("New Location [6, 4]:")
print(f" -> Cityblock Distance: {new_cityblock} blocks")
print(f" -> Estimated Fuel: {float(estimated_fuel):.1f} Liters")
