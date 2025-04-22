# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:56:09 2025

@author: evert
"""

import numpy as np
import random
import matplotlib.pyplot as plt

random_seed = random.seed(77)
n = 7
x = [random.random() for _ in range(n)]
y = [random.random() for _ in range(n)] 

nodes = np.array([x,y]).T

plt.figure(1)
plt.scatter(x, y, marker='o')  
plt.title('Data Points')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()  



