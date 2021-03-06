# Graph representation of the labyrinth

class Graph:
    def __init__(self):
        # graph of challenge 1 labyrinth
        self.graph = {
            0: [6],
            1: [2, 7],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4],
            6: [0, 7],
            7: [1, 6, 13],
            12: [18],
            13: [7,14],
            14: [13, 20],
            15: [16],
            16: [15, 17],
            17: [16],
            18: [12, 19, 24],
            19: [18, 20, 25],
            20: [14, 19, 21],
            21: [20, 27],
            22: [16, 28],
            24: [18, 30],
            25: [19,31],
            27: [21, 28, 33],
            28: [22, 27, 29, 34],
            29: [28, 35],
            30: [24],
            31: [25,32],
            32: [31, 33],
            33: [27,32],
            34: [28],
            35: [29]
        }
    
    def getgraph(self):
        return self.graph

    def getvalue(self, i):
        return self.graph[i]
