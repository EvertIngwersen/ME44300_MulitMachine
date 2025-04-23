# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:56:09 2025

@author: evert
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt

def do_edges_intersect(p1, p2, q1, q2):
    def ccw(a, b, c):
        return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

random.seed(5773)
n = 40
m = 100

x = [random.random() * m for _ in range(n)]
y = [random.random() * m for _ in range(n)]
nodes = np.array([x, y]).T
integer_list = list(range(n))

edges = set()
vertices_dict = {i: [] for i in range(n)}

for i in range(n):
    candidates = [j for j in integer_list if j != i]
    random.shuffle(candidates)
    max_edges_this_node = random.randint(1, 4)
    added = 0
    for j in candidates:
        if added >= max_edges_this_node:
            break
        p1, p2 = nodes[i], nodes[j]
        intersects = False
        for a, b in edges:
            q1, q2 = nodes[a], nodes[b]
            if len({i, j, a, b}) == 4 and do_edges_intersect(p1, p2, q1, q2):
                intersects = True
                break
        if not intersects:
            edges.add((i, j))
            vertices_dict[i].append(j)
            added += 1

# Plotting
plt.figure()
plt.scatter(x, y, marker='o')
plt.title('Planar Graph with No Crossing Edges')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

for i in range(n):
    plt.text(x[i] + 0.1, y[i] + 0.1, str(i), fontsize=9)

for i, j in edges:
    plt.plot([x[i], x[j]], [y[i], y[j]], color='gray')

plt.xlim(0, m)
plt.ylim(0, m)
plt.show()
        
distance_matrix = np.full((n, n), np.nan)

for i in range(n):
    for j in vertices_dict[i]:
        dist = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
        distance_matrix[i, j] = dist
        distance_matrix[j, i] = dist

for i in range(n):
    distance_matrix[i,i] = 0











