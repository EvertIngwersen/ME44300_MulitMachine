# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 12:44:58 2025

@author: evert
"""

#import libraries

import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 10, 1000)  # From 0 to 10 seconds, 1000 samples

# Inputs u1(t) and u2(t)
u1 = np.sin(t)
u2 = np.cos(t)

# Coefficients of the system
b11, b12 = 1.0, 2.0
b21, b22 = 3.0, 4.0

# Compute outputs x1(t) and x2(t)
x1 = b11 * u1 + b12 * u2
x2 = b21 * u1 + b22 * u2

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, x1, label='x₁(t)')
plt.plot(t, x2, label='x₂(t)')
plt.xlabel('Time t')
plt.ylabel('Output')
plt.title('Static System Output over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
