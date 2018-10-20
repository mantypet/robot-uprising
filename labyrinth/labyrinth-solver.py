from graph import *
import math
import operator

class Dijkstra:
    def __init__(self, start, goal):
        self.map = Graph()
        self.distance = [] # indeksin solmun etaisyys lahtoon
        self.path = [] # indeksin solmua edeltävä solmu toistaiseksi lyhimmällä polulla
        self.s = []
        self.start = start
        self.goal = goal
        for i in range(36):
            self.distance.append(1000)
            self.path.append(-1)
        self.distance[start] = 0

    def heuristic(self, start, goal):
        startx = math.floor(start / 6)
        starty = start% 6
        goalx = math.floor(goal / 6)
        goaly = goal % 6

        distx = abs(startx-goalx)
        disty = abs(starty - goaly)

        return distx+disty


    def relax(self, u, v):
        if self.distance[v] > self.distance[u] + self.heuristic(u, v):
            self.distance[v] = self.distance[u] + self.heuristic(u, v)
            self.path[v] = u

    def dij(self):
        keys = list(self.map.getgraph().keys())
        while(len(self.s) != len(keys)):
            left = []
            for member in keys:
                if member not in self.s:
                    left.append(member)
            shortest = left[0]
            for node in left:
                if self.distance[node] < self.distance[shortest]:
                    shortest = node
            self.s.append(shortest)
            for neigh in self.map.getvalue(shortest):
                self.relax(shortest, neigh)
        self.shortest_path(self.goal)

    def shortest_path(self, goal):
        u = self.path[goal]
        items = []
        items.append(goal)
        while u != self.start:
            items.append(u)
            u = self.path[u]
        items.append(self.start)
        while len(items) != 0:
            u = items.pop()
            print(u)
            
