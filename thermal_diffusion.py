import numpy as np

# 1. Setup Parameters
thickness_inches = 10.0
num_nodes = 6
space_grid = np.linspace(0.0, thickness_inches, num_nodes)  # [0, 2, 4, 6, 8, 10] inches

# Timeline: 0 to 10 minutes with 2-minute intervals -> [0, 2, 4, 6, 8, 10]
time_steps = np.arange(0, 11, 2)

num_rows = len(time_steps)  # 6 time steps
num_cols = len(space_grid)  # 6 physical nodes

temp_matrix = np.zeros((num_rows, num_cols))

# Initial Temperatures at t = 0 mins
# Node 0 (0-inch pan) = 180°C, rest of internal pizza = 20°C
initial_temps = np.array([180.0, 20.0, 20.0, 20.0, 20.0, 20.0])
temp_matrix[0, :] = initial_temps

thermal_diffusivity = 0.20

# 2. Simulation Loop (Explicit Finite Difference)
for t in range(1, num_rows):
    # Copy previous state
    temp_matrix[t, :] = temp_matrix[t - 1, :]

    # Update internal nodes (Node 1 to Node 4)
    for i in range(1, num_cols - 1):
        conduction = thermal_diffusivity * (
            temp_matrix[t - 1, i - 1]
            - 2 * temp_matrix[t - 1, i]
            + temp_matrix[t - 1, i + 1]
        )
        temp_matrix[t, i] = temp_matrix[t - 1, i] + conduction

# 3. Display the Matrix Output
print("--- TEMPERATURE MATRIX (°C) ---")
print("Rows: t = [0m, 2m, 4m, 6m, 8m, 10m]")
print("Cols: x = [0in, 2in, 4in, 6in, 8in, 10in]\n")
print(np.round(temp_matrix, 3))
print("\n" + "=" * 50 + "\n")

# 4. Analysis and Requirements Check

# Requirement A: Absolute Extreme Temperatures Logged Anywhere
min_temp = np.min(temp_matrix)
max_temp = np.max(temp_matrix)

# Requirement B: Average Temperature at Minute 10 (Final Row)
avg_temp_final = np.mean(temp_matrix[-1, :])

# Requirement C: Check for Breached Burning Threshold (> 75°C) in Internal Dough (Cols 1 to 5)
internal_temps = temp_matrix[:, 1:]  # Exclude Col 0 (the 180°C pan)
burned_coords = []

for t_idx in range(num_rows):
    for col_idx in range(1, num_cols):
        val = temp_matrix[t_idx, col_idx]
        if val > 75.0:
            time_val = time_steps[t_idx]
            pos_val = space_grid[col_idx]
            burned_coords.append((time_val, pos_val, val))

# Requirement D: Check Innermost Core / Dough Progress
# (Node 1 at 2-inch or Node 2 at 4-inch vs 50°C target by Minute 10)
core_temp_min10 = temp_matrix[-1, 1]  # At 2-inch position at Minute 10

# Display Findings
print("--- ANALYSIS FINDINGS ---")
print(f"1. Extreme Temperatures Logged:")
print(f"   - Lowest:  {min_temp}°C")
print(f"   - Highest: {max_temp}°C")

print(
    f"\n2. Average Overall Temperature at Minute 10: {avg_temp_final:.2f}°C"
)

print("\n3. Burning Threshold Check (> 75°C for internal elements):")
if len(burned_coords) > 0:
    for t_m, pos_in, temp in burned_coords:
        print(
            f"   BREACHED! At {t_m} mins, Position {pos_in:.0f}-inch reached {temp:.3f}°C"
        )
else:
    print(
        "  SAFE! No internal dough/cheese exceeded 75°C during baking."
    )

print("\n4. Cooking Safety Standard Check (Target >= 50°C at Core):")
print(f"   - Temperature at 2-inch mark at Minute 10: {core_temp_min10:.3f}°C")
if core_temp_min10 >= 50.0:
    print("  PASSED! The inner dough successfully reached at least 50°C.")
else:
    print(
        f"   FAILED! Core only reached {core_temp_min10:.3f}°C (Needs >= 50°C to be safe to eat)."
    )