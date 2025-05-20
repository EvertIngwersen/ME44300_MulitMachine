# -*- coding: utf-8 -*-
"""
Created on Fri May 16 13:37:53 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import do_mpc
from casadi import *

# Define system parameters
m = 23.8
ma = 2
Rs = 1.44
Ts = 1.0  # Discrete time step

# System matrices (discrete-time)
A = 1 + Rs / (m + ma)
B = 1 / (m + ma)
C = 1
D = 0

# Reference and disturbance parameters
Vref = 0.1
Vc = 0.0
tau_wave_amp = 0.0
tau_wave_freq = 0.0

# Operational constraints
u_min, u_max = 0.0, 5.0   # tau bounds
y_min, y_max = 0.0, 0.2   # velocity bounds

# --- Define the model ---
model_type = 'discrete'
model = do_mpc.model.Model(model_type)

# States and input
v = model.set_variable(var_type='_x', var_name='v')   # velocity
u = model.set_variable(var_type='_u', var_name='u')   # thrust

# Dynamics
model.set_rhs('v', A * v + B * u)
model.setup()

# --- MPC setup ---
def get_mpc(model, horizon, alpha, beta):
    mpc = do_mpc.controller.MPC(model)
    setup_mpc = {
        'n_horizon': horizon,
        't_step': Ts,
        'store_full_solution': True
    }
    mpc.set_param(**setup_mpc)

    # Objective function
    mterm = alpha * (v - Vref)**2
    lterm = alpha * (v - Vref)**2 + beta * u**2
    mpc.set_objective(mterm=mterm, lterm=lterm)

    mpc.set_rterm(u=beta)

    # Constraints
    mpc.bounds['lower', '_u', 'u'] = u_min
    mpc.bounds['upper', '_u', 'u'] = u_max
    mpc.bounds['lower', '_x', 'v'] = y_min
    mpc.bounds['upper', '_x', 'v'] = y_max

    mpc.setup()
    return mpc

# MPC controller
alpha = 100
beta = 0
horizon = 2
mpc = get_mpc(model, horizon, alpha, beta)

# --- Simulator setup ---
simulator = do_mpc.simulator.Simulator(model)
simulator.set_param(t_step=Ts)
simulator.setup()

# --- Initial state ---
x0 = np.array([[0.0]])  # Initial velocity = 0
mpc.x0 = x0
simulator.x0 = x0
model.x0 = x0

mpc.set_initial_guess()

# --- Simulation loop ---
t_sim = 100
x_history = []
u_history = []
time = []

for k in range(t_sim):
    u0 = mpc.make_step(x0)
    x0 = simulator.make_step(u0)

    x_history.append(float(x0[0]))
    u_history.append(float(u0[0]))
    time.append(k * Ts)

# --- Plot results ---
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(time, x_history, label='Velocity (v)', color='blue')
plt.axhline(Vref, color='green', linestyle='--', label='Reference')
plt.title('System Output (Velocity)')
plt.ylabel('Velocity [m/s]')
plt.grid(True)
plt.legend()
plt.ylim(0, 0.25)

plt.subplot(2, 1, 2)
plt.plot(time, u_history, label='Control Input (u)', color='orange')
plt.title('Control Input (Thrust)')
plt.xlabel('Time [s]')
plt.ylabel('Thrust')
plt.grid(True)
plt.legend()
plt.ylim(0, 5.5)

plt.tight_layout()
plt.show()

