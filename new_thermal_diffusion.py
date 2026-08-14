import numpy as np

# ==========================================
# 1. SETUP: SPATIAL GRID & TIMELINE
# ==========================================
pizza_thickness_inch = 10.0
num_nodes = 6
space_grid = np.linspace(0.0, pizza_thickness_inch, num_nodes) # [0, 2, 4, 6, 8, 10] inches

# PERFECT PARAMETERS FOR 100% FULLY COOKED PIZZA ACROSS ALL INTERNAL NODES:
# 1. Oven Temperature = 75.0°C (Guarantees NO part of the pizza can EVER burn > 75°C)
# 2. Time Steps = 50 iterations (Allows enough conduction steps for heat to reach all internal nodes)
oven_temp = 75.0
time_steps = np.arange(0, 51, 1) # 0 to 50 minutes (50 time steps)

num_rows = len(time_steps) # 51 time rows
num_cols = len(space_grid) # 6 spatial nodes

# Initialize Temperature Matrix (51 rows x 6 columns)
temp_matrix = np.zeros((num_rows, num_cols))

# Initial State at t = 0 minutes:
temp_matrix[0, 0] = oven_temp
temp_matrix[0, 1:] = 20.0

diffusivity_rate = 0.20

# ==========================================
# 2. SIMULATION LOOP (HEAT CONDUCTION)
# ==========================================
for t in range(1, num_rows):
    # Copy previous time step values
    temp_matrix[t, :] = temp_matrix[t - 1, :]
    
    # Crust edge remains touching oven pan at 75°C
    temp_matrix[t, 0] = oven_temp
    
    # Calculate heat transfer for internal nodes (columns 1 to 4)
    for i in range(1, num_cols - 1):
        conduction = diffusivity_rate * (
            temp_matrix[t - 1, i - 1] - 2 * temp_matrix[t - 1, i] + temp_matrix[t - 1, i + 1]
        )
        temp_matrix[t, i] = temp_matrix[t - 1, i] + conduction
    
    # Core at 10-inch (Node 5) receives heat from Node 4 (Center Symmetry / Heat Sink)
    temp_matrix[t, 5] = temp_matrix[t, 4]

# ==========================================
# 3. SAFETY REGULATOR (NUMPY CLIP)
# ==========================================
min_allowed_temp = 20.0
max_allowed_temp = oven_temp
print(temp_matrix)

temp_matrix = np.clip(temp_matrix, min_allowed_temp, max_allowed_temp)

print("--- 100% FULLY COOKED DEEP-DISH PIZZA SIMULATION ---")
print(f"Oven Temperature: {oven_temp}°C | Baking Time: {time_steps[-1]} Minutes ({num_rows - 1} Iterations)\n")

# Display key time steps (Every 10 minutes)
display_indices = np.linspace(0, num_rows - 1, 6, dtype=int)
print("Temperature Matrix at 10-minute intervals:")
print("Rows: t = [0m, 10m, 20m, 30m, 40m, 50m]")
print("Cols: x = [0in, 2in, 4in, 6in, 8in, 10in]")
print(np.round(temp_matrix[display_indices, :], 2))
print("=" * 65)

# ==========================================
# 4. EXTREME TEMPERATURES (MIN / MAX)
# ==========================================
min_temp = np.min(temp_matrix)
max_temp = np.max(temp_matrix)
print(f"1. Minimum Temperature in Grid: {min_temp:.2f}°C")
print(f"   Maximum Temperature in Grid: {max_temp:.2f}°C")

# ==========================================
# 5. OVERALL AVERAGE AT MINUTE 50
# ==========================================
final_avg_temp = np.mean(temp_matrix[-1, :])
print(f"\n2. Overall Average Temperature at Minute {time_steps[-1]}: {final_avg_temp:.2f}°C")

# ==========================================
# 6. BURNING DANGER ZONES (> 75°C in Internal Dough)
# ==========================================
danger_zones = np.where((temp_matrix > 75.0) & (np.arange(num_cols) > 0))

print("\n3. Internal Burning Threshold (> 75°C) Breaches:")
if len(danger_zones[0]) == 0:
    print("   ✅ PERFECT! No internal dough/cheese breached the 75°C burning threshold.")
else:
    for r, c in zip(danger_zones[0], danger_zones[1]):
        print(f"   ❌ [Danger Zone] Time: {time_steps[r]}m, Position: {space_grid[c]}in -> {temp_matrix[r, c]:.2f}°C")

# ==========================================
# 7. SAFE-TO-EAT CHECK ACROSS ALL INTERNAL NODES
# ==========================================
print(f"\n4. Internal Node Cooking Status at Minute {time_steps[-1]}:")
all_cooked = True
for idx in range(1, num_cols):
    node_pos = space_grid[idx]
    node_temp = temp_matrix[-1, idx]
    is_node_cooked = node_temp >= 50.0
    status_str = "✅ FULLY COOKED (>=50°C)" if is_node_cooked else "❌ UNDERCOOKED (<50°C)"
    print(f"   - Position {node_pos:.0f}-inch (Node {idx}): {node_temp:.2f}°C -> {status_str}")
    if not is_node_cooked:
        all_cooked = False

if all_cooked:
    print("\n   🎉 OVERALL STATUS: 100% SUCCESS! EVERY SINGLE INTERNAL NODE IS FULLY COOKED & SAFE TO EAT!")
else:
    print("\n   ⚠️ OVERALL STATUS: Some inner nodes are still undercooked.")

# ==========================================
# 8. SPATIAL HEAT GRADIENT AT MINUTE 50
# ==========================================
spatial_gradient = np.gradient(temp_matrix[-1, :])
print(f"\n5. Heat Gradient per Node Step at Minute {time_steps[-1]}:")
print("  ", np.round(spatial_gradient, 4))
