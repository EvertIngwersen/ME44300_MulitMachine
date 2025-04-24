# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 13:20:44 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

m = 1000            # mass of the car [kg]
b = 50              # damping [Ns/m]

Kp = 500            # proportional gain
desired_speed = 25 

t_end = 20
dt = 0.01

t = np.arange(0, t_end, dt)





