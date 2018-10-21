# Dijkstra algorithm

from labyrinth.graph import *
import math
import operator

class Dijkstra:
    def __init__(self, start, goal):
        self.map = Graph()
        self.distance = []  # distance of index node to start
        self.path = []      # shortest path for node before index node
        self.s = []         # visited nodes
        self.start = start  # start node
        self.goal = goal    # goal node
        for i in range(36): # initialize all distances
            self.distance.append(1000)
            self.path.append(-1)
        self.distance[start] = 0 # distance to start is zero

    def heuristic(self, start, goal):   # manhattan distance
        startx = math.floor(start / 6)  # 1 dimensional coordinate to 2d row coordinate
        starty = start% 6               # 1 dimensional coordinate to 2d column coordinate
        goalx = math.floor(goal / 6)
        goaly = goal % 6

        distx = abs(startx-goalx)       # distance between rows
        disty = abs(starty - goaly)     # distance between colmuns

        return distx + disty


    def relax(self, u, v):
        if self.distance[v] > self.distance[u] + self.heuristic(u, v): # update distance for next node v 
            self.distance[v] = self.distance[u] + self.heuristic(u, v) # if found better path
            self.path[v] = u

    def dij(self):
        keys = list(self.map.getgraph().keys()) # all nodes you can reach
        while(len(self.s) != len(keys)):        # while there are unvisited nodes
            left = []                           # nodes not visited
            for member in keys:                 # from all nodes
                if member not in self.s:        # choose those not visited
                    left.append(member)
            shortest = left[0]                  # initial value for shortest
            for node in left:                   # compare all nodes and...
                if self.distance[node] < self.distance[shortest]: # ...find shortest
                    shortest = node
            self.s.append(shortest)             # add shortest distance node to visited
            for neigh in self.map.getvalue(shortest): # update distances for neighbours of shortest distance node
                self.relax(shortest, neigh)
        # return in 2 dimensional coordinates shortest path for asked goal from start
        return self.backto2d(self.shortest_path(self.goal))

    def backto2d(self, items): # change 1 dimensional coordinates to 2d coordinates for pathlist
        coordinates = [] # 2d table
        index = 0
        size = len(items)
        for i in range(size): # initialize 2d table to empty tables
            innertable = []
            coordinates.append(innertable)
        while len(items) != 0: # add nodes in path to 2d table
            u = items.pop()
            row = math.floor(u/6)   # count 2d row
            col = u % 6             # count 2d column
            templist = []
            templist.append(row)
            templist.append(col)
            coordinates[index]=templist # add coordinates to 2d table, coordinates[i] tells i-th node in path
            index += 1
        # return 2d table with coordinates
        return(coordinates)


    def shortest_path(self, goal): # reverse path from goal to start
        u = self.path[goal]
        items = []
        items.append(goal)
        while u != self.start:
            items.append(u)
            u = self.path[u]
        items.append(self.start)

        return items
            
