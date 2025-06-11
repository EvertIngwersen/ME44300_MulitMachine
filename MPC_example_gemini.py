# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 13:57:09 2025

@author: evert
"""

import numpy as np
import cvxpy as cp

# --- 1. System Definition ---
# For a simple discrete-time integrator: x_k+1 = x_k + u_k
# This is equivalent to:
# A_matrix = np.array([[1.]])
# B_matrix = np.array([[1.]])
# C_matrix = np.array([[1.]]) # Output is the state itself

# --- 2. MPC Parameters ---
HORIZON_PREDICTION = 10 # Np: How many steps to predict into the future
HORIZON_CONTROL = 5     # Nc: How many control inputs to optimize (Nc <= Np)
DT = 1.0                # Time step (for simulation, not directly in MPC formulation for integrator)

# Weighting matrices for the cost function
Q = np.array([[10.0]])  # Weight for tracking error (state error)
R = np.array([[0.1]])   # Weight for control effort (input magnitude)

# Constraints (optional, but crucial for real MPC)
U_MAX = 1.0             # Maximum control input
U_MIN = -1.0            # Minimum control input
X_MAX = 5.0             # Maximum state value (e.g., position limit)
X_MIN = -5.0            # Minimum state value

# --- 3. Simulation Setup ---
SIMULATION_STEPS = 50
current_state = np.array([0.0]) # Initial state of the system
reference_trajectory = np.array([3.0] * SIMULATION_STEPS) # Constant reference for simplicity

# Store results
states_history = [current_state.flatten()]
inputs_history = []
references_history = [reference_trajectory[0]]

print("Starting MPC simulation...")

# --- 4. MPC Loop (Receding Horizon) ---
for k in range(SIMULATION_STEPS):
    # --- a. Define Optimization Variables ---
    # These are the future control inputs we want to find
    u_vars = cp.Variable((HORIZON_CONTROL, 1))
    # These are the predicted future states based on the control inputs
    x_predicted = cp.Variable((HORIZON_PREDICTION + 1, 1))

    # --- b. Define the Cost Function ---
    cost = 0
    constraints = [x_predicted[0] == current_state] # Initial state constraint

    for i in range(HORIZON_PREDICTION):
        # Predict the next state based on the current predicted state and control input
        # Note: We use u_vars[min(i, HORIZON_CONTROL - 1)] because control inputs
        # are constant after the control horizon.
        u_at_i = u_vars[min(i, HORIZON_CONTROL - 1)]
        constraints += [x_predicted[i+1] == x_predicted[i] + u_at_i]

        # Add tracking error to cost
        # We need to ensure reference_trajectory[k + i] is used for prediction step i
        if (k + i) < SIMULATION_STEPS: # Ensure we don't go out of bounds for reference
             cost += cp.quad_form(x_predicted[i+1] - reference_trajectory[k + i], Q)
        else: # If prediction goes beyond available reference, use the last reference value
             cost += cp.quad_form(x_predicted[i+1] - reference_trajectory[-1], Q)


        # Add control effort penalty to cost (only for control horizon)
        if i < HORIZON_CONTROL:
            cost += cp.quad_form(u_at_i, R)

        # --- c. Add Constraints ---
        constraints += [U_MIN <= u_at_i, u_at_i <= U_MAX]
        constraints += [X_MIN <= x_predicted[i+1], x_predicted[i+1] <= X_MAX]


    # --- d. Solve the Optimization Problem ---
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve(solver='OSQP') # OSQP is a good, fast solver for QPs

    if problem.status not in ["optimal", "optimal_inaccurate"]:
        print(f"Warning: Problem status is {problem.status} at step {k}. Controller might be infeasible.")
        # Fallback: if not optimal, maybe just apply no control or previous control
        applied_input = np.array([0.0]) # Or some emergency value
    else:
        # --- e. Apply the First Optimal Control Input ---
        applied_input = u_vars.value[0] # Take only the first optimized input

    inputs_history.append(applied_input.flatten())

    # --- f. Simulate the System (external process) ---
    # In a real system, this would be the actual physical process
    current_state = current_state + applied_input
    states_history.append(current_state.flatten())
    references_history.append(reference_trajectory[min(k + 1, SIMULATION_STEPS - 1)])


    if k % 10 == 0:
        print(f"Step {k}: Current State = {current_state.flatten()[0]:.2f}, Applied Input = {applied_input.flatten()[0]:.2f}, Reference = {reference_trajectory[k]:.2f}")

print("\nSimulation Finished.")

# --- 5. Plotting Results (Requires matplotlib) ---
try:
    import matplotlib.pyplot as plt

    states_history = np.array(states_history).flatten()
    inputs_history = np.array(inputs_history).flatten()
    references_history = np.array(references_history).flatten()

    time = np.arange(SIMULATION_STEPS + 1)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time, states_history, label='Actual State (x)')
    plt.plot(time, references_history, 'r--', label='Reference (r)')
    plt.title('MPC Control of Simple Integrator System')
    plt.ylabel('State Value')
    plt.xlabel('Time Step')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.step(time[:-1], inputs_history, where='post', label='Control Input (u)')
    plt.axhline(y=U_MAX, color='g', linestyle=':', label='U_MAX')
    plt.axhline(y=U_MIN, color='g', linestyle=':', label='U_MIN')
    plt.ylabel('Control Input')
    plt.xlabel('Time Step')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

except ImportError:
    print("\nMatplotlib not found. Install it (`pip install matplotlib`) to visualize results.")