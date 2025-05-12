# -*- coding: utf-8 -*-
"""
Created on Mon May 12 10:07:37 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

# Time settings
dt = 0.1  # time step (s)
T = 200    # total time (s)
N = int(T / dt)


# ======= 1. Longitudinal Model (Mainline) =======
s = 0.0         # initial position (m)
v = 0.0         # initial velocity (m/s)
a = 0.5         # constant acceleration (m/s²)

s_hist = []
v_hist = []

for _ in range(N):
    s_hist.append(s)
    v_hist.append(v)
    
    s += v * dt
    v += a * dt

# ======= 2. 2D Bicycle Model (Terminal) =======
x = 0.0         # initial x-position
y = 0.0         # initial y-position
theta = 0.0     # initial heading (rad)
v2 = 2.0        # constant speed (m/s)
L = 5.0         # wheelbase (m)
delta = 0.2     # steering angle (rad)

x_hist = []
y_hist = []

for _ in range(N):
    x_hist.append(x)
    y_hist.append(y)
    
    x += v2 * np.cos(theta) * dt
    y += v2 * np.sin(theta) * dt
    theta += (v2 / L) * np.tan(delta) * dt

# ======= Plotting =======
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot longitudinal model
axs[0].plot(np.linspace(0, T, N), s_hist, label='Position (s)')
axs[0].plot(np.linspace(0, T, N), v_hist, label='Velocity (v)')
axs[0].set_title("Mainline Longitudinal Motion")
axs[0].set_xlabel("Time (s)")
axs[0].legend()
axs[0].grid(True)

# Plot 2D terminal path
axs[1].plot(x_hist, y_hist, label='Path')
axs[1].set_title("Terminal 2D Motion")
axs[1].set_xlabel("X (m)")
axs[1].set_ylabel("Y (m)")
axs[1].axis('equal')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
