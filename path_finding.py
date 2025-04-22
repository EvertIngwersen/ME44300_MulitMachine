# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:56:09 2025

@author: evert
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt

random_seed = random.seed(77)
n = 10 # amount of nodes
m = 10 # size of the graph 

x = [random.random()*m for _ in range(n)]
y = [random.random()*m for _ in range(n)] 

nodes = np.array([x,y]).T

integer_list = list(range(0, n))
vertices_dict = {}

for i in range(n):
    num_elements = random.randint(1, 3)  # Random number between 1 and max_connections
    vertices_dict[i] = random.sample(integer_list, num_elements)

for key in vertices_dict:
    vertices_dict[key] = [x for x in vertices_dict[key] if x != key]
    if len(vertices_dict[key]) == 0:
        vertices_dict[key] = [random.randint(0, n)] 
    
    
plt.figure(1)
plt.scatter(x, y, marker='o')  
plt.title('Graph with Connected Nodes')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
# Add node indices
for i in range(n):
    plt.text(x[i] + 0.1, y[i] + 0.1, str(i), fontsize=9, color='black')
# Draw connections
for node, connections in vertices_dict.items():
    for neighbor in connections:
        x_coords = [nodes[node][0], nodes[neighbor][0]]
        y_coords = [nodes[node][1], nodes[neighbor][1]]
        plt.plot(x_coords, y_coords, color='gray', linewidth=1)
# Set fixed axis limits
plt.xlim(0, m)
plt.ylim(0, m)
plt.show()

distance_matrix = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        distance_matrix[i,j] = math.sqrt(((x[i]-x[j])**2)+(y[i]-y[j])**2)
        


        












