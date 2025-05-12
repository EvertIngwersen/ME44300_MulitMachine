# -*- coding: utf-8 -*-
"""
Created on Mon May 12 12:08:22 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# System Parameters
M = 50000       #train mass
b = 1000        #rolling resistance 
c = 50          #aero drag coef
g = 9.81
α = 0           #slope
dt = 0.1
N = 10          #MPC horizon
T = 50          #total time
steps = int(T / dt)

# Constraints
P_min = 0
P_max = 5e6

# Cost weights



