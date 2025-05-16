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

# State-space system (converted to discrete)
sysc = ctrl.ss(A, B, C, D)
sysd = ctrl.c2d(sysc, Ts)

# Reference and disturbance parameters
Vref = 0.1
Vc = 0.0
tau_wave_amp = 0.0
tau_wave_freq = 0.0

# Operational constraints
u_min, u_max = 0.0, 5.0   # tau bounds
y_min, y_max = 0.0, 0.2   # velocity bounds

# Define the model using do-mpc
model_type = 'discrete'  # Because Ts = 1
model = do_mpc.model.Model(model_type)

# States, inputs, outputs
v = model.set_variable(var_type='_x', var_name='v')   # velocity (state)
u = model.set_variable(var_type='_u', var_name='u')   # thrust (control input)

# System dynamics
model.set_rhs('v', A * v + B * u)

# Setup model
model.setup()

# MPC controller setup
def get_mpc(model, horizon, alpha, beta):
    mpc = do_mpc.controller.MPC(model)
    setup_mpc = {
        'n_horizon': horizon,
        't_step': Ts,
        'store_full_solution': True
    }
    mpc.set_param(**setup_mpc)

    # Objective
    mterm = alpha * (v - Vref)**2
    lterm = alpha * (v - Vref)**2 + beta * u**2
    mpc.set_objective(mterm=mterm, lterm=lterm)

    mpc.set_rterm(u=beta)  # Penalize control effort

    # Constraints
    mpc.bounds['lower', '_u', 'u'] = u_min
    mpc.bounds['upper', '_u', 'u'] = u_max
    mpc.bounds['lower', '_x', 'v'] = y_min
    mpc.bounds['upper', '_x', 'v'] = y_max

    mpc.setup()
    return mpc

# Define both MPC controllers
alpha = 100
beta = 0

horizon = 2
tend = 100

mpc_short = get_mpc(model, horizon, alpha, beta)
mpc_long = get_mpc(model, tend, alpha, beta)

# Note: Simulation loop not included — would require setting up simulator and initial conditions.
