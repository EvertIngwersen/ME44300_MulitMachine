# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 15:23:09 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
gamma = 1       # Step size
epsilon = 0.1       # Convergence threshold
max_iters = 50 # Max number of iterations

# Initialization
u_A = [-5.0]         # Initial guess for agent A
u_B = [-100.0]        # Initial guess for agent B
lambda_in_BA = [0]  # Dual variable

# Store history for plotting
history_u_A = [u_A[0]]
history_u_B = [u_B[0]]
history_lambda = [lambda_in_BA[0]]

# Start iterations
for s in range(max_iters):
    # Agent A optimization
    uB_prev = u_B[-1]
    lam = lambda_in_BA[-1]

    # Minimize: J_A = u_A^2 + lam*u_A + 0.5*(u_A - uB_prev)^2
    # Derivative: 2*u_A + lam + (u_A - uB_prev) = 0
    # => 3*u_A + lam - uB_prev = 0 => u_A = (uB_prev - lam) / 3
    uA_new = (uB_prev - lam) / 3
    u_A.append(uA_new)

    # Agent B optimization
    uA_prev = u_A[-2]
    # Minimize: J_B = u_B^2 - lam*u_B + 0.5*(u_B - uA_prev)^2
    # Derivative: 2*u_B - lam + (u_B - uA_prev) = 0
    # => 3*u_B - lam - uA_prev = 0 => u_B = (lam + uA_prev) / 3
    uB_new = (lam + uA_prev) / 3
    u_B.append(uB_new)

    # Update dual variable
    lambda_new = lam + gamma * (uB_new - uA_new)
    lambda_in_BA.append(lambda_new)

    # Store history
    history_u_A.append(uA_new)
    history_u_B.append(uB_new)
    history_lambda.append(lambda_new)

    # Check convergence
    if abs(lambda_new - lam) < epsilon:
        print(f"Converged at iteration {s+1}")
        break

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axs[0].plot(history_u_A, marker='o', label='u_A (Agent A)')
axs[0].plot(history_u_B, marker='s', label='u_B (Agent B)')
axs[0].set_ylabel('Control Inputs')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(history_lambda, marker='x', color='purple', label='λ_in_BA')
axs[1].set_ylabel('Dual Variable')
axs[1].set_xlabel('Iteration')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
