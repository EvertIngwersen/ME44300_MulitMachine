# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 13:20:44 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

m = 1000            # mass of the car [kg]
b = 50              # damping [Ns/m]

Kp = 100 
Ki = 10           # proportional gain


t_end = 10
dt = 0.01

t = np.arange(0, t_end, dt)

# initial conditions

v = 0
u = 0 
integral = 0
v_history = []
desired_history = []


for time in t:
    desired_speed = time**2 + np.sin(3*time)  # Sine wave: oscillates between 15 and 25
    desired_history.append(desired_speed)

    error = desired_speed - v
    integral += error * dt
    u = Kp * error + Ki * integral

    dv_dt = (u - b * v) / m
    v += dv_dt * dt
    v_history.append(v)
    
plt.figure()
plt.plot(t, v_history, label='Vehicle Speed')
plt.plot(t, desired_history, 'r--', label='Desired Speed')
plt.title('Cruise Control System Response')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.grid(True)
plt.show()

