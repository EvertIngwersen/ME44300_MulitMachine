# -*- coding: utf-8 -*-
"""
Created on Mon May 12 12:08:22 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# System parameters
M = 50000       #train mass
b = 1000        #rolling resistance 
c = 50          #aero drag coef
g = 9.81
α = 0           #slope
dt = 0.5
ε = 0.01
N = 10          #MPC horizon
T = 500          #total time
steps = int(T / dt)

# Constraints
P_min = 0
P_max = 5e6

# Cost weights
Q_v = 1         #speed tracking
R = 1e-7        #power usage

# Reference speed
v_ref = 3      #reference speed

# Initial state
s_now = 0
v_now = 0.5

# History logs
s_hist = [s_now]
v_hist = [v_now]
u_hist = []

# Non-linear dynamics
def train_dynamics(s,v,P):
    v_safe = max(v,ε)
    Fw = b * v_safe + c * v_safe**2 + M * g * np.sin(α)
    a = (P/v_safe - Fw) / M
    s_next = s + dt * v_safe
    v_next = v + dt * a
    return s_next, v_next

# Cost function for MPC
def mpc_cost(P_seq, s0, v0):
    s = s0
    v = v0
    cost = 0.0
    for k in range(N):
        P = P_seq[k]
        s, v = train_dynamics(s, v, P)
        cost += Q_v * (v - v_ref)**2 + R * P**2
    return cost

# Bounds for optimizer
bounds = [(P_min, P_max) for _ in range(N)]

# MPC loop
for t in range(steps - 1):
    x0 = np.ones(N) * 2e6  # initial guess: 2 MW

    res = minimize(
        mpc_cost, x0, args=(s_now, v_now),
        bounds=bounds, method='SLSQP', options={'disp': False}
    )

    P_opt = res.x[0]
    s_next, v_next = train_dynamics(s_now, v_now, P_opt)

    # Store
    u_hist.append(P_opt)
    s_hist.append(s_next)
    v_hist.append(v_next)

    # Update state
    s_now, v_now = s_next, v_next

# Convert to arrays for plotting
time = np.linspace(0, T, steps)
s_hist = np.array(s_hist)
v_hist = np.array(v_hist)
u_hist = np.array(u_hist)

# Plot results
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(time, v_hist, label='Speed (m/s)')
plt.axhline(v_ref, color='r', linestyle='--', label='Reference')
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.grid()
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(time[:-1], u_hist / 1e6, label='Power Input (MW)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Power (MW)')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()















