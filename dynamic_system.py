# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 12:44:58 2025

@author: evert
"""

import numpy as np
import math
import matplotlib.pyplot as plt

b11, b12 = 1.0, 2.0
b21, b22 = 3.0, 4.0
u1_t, u2_t = 5.0, 6.0

u = np.array([u1_t, u2_t])
B = np.array([
    [b11, b12],
    [b21, b22]
])

x = B @ u
print("x1(t):", x[0])
print("x2(t):", x[1])

#test comment for commit

