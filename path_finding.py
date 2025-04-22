# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:56:09 2025

@author: evert
"""

import numpy as np
import random
import matplotlib.pyplot as plt

random_seed = random.seed(77)
n = 5
x = [random.random() for _ in range(n)]
y = [random.random() for _ in range(n)] 

nodes = np.array([x,y]).T


