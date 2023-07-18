from collections import deque
import heapq
import random

dirx = [-1, 1, 0, 0]
diry = [0, 0, -1, 1]

opp_dirx = [1, -1, 0, 0]
opp_diry = [0, 0, 1, -1]

"""
In the visited array:
0 -> unexplored
1 -> visited, but only water found
2 -> Ship identified
"""
# matrix size fixed to 10x10
# boat sizes fixed : 5, 4, 3, 3, 2 --> not considerd as of now || Total = 17
class CodeComp:
    def __init__(self, n, t, region):
        self.n = n              # number of shots allowed to fire at once.
        self.t = t              # total number of shots
        self.region = region
        self.visited = [[0 for i in range(10)] for j in range(10)]
        self.result = 0

        self.pos = [[0, 4, 4]]  # starting position # priority, x, y
        heapq.heapify(self.pos) # min heap by default

    def isValid(self, x, y):
        return x >= 0 and y >= 0 and x < 10 and y < 10

    def fireShotsAndUpdateResponse(self):
        fired = 0
        response = []       # p, x, y, result
        while(len(self.pos) > 0 and fired < self.n and self.t > 0):
            p, x, y = heapq.heappop(self.pos)
            self.t -= 1
            fired += 1
            if(self.region[x][y] == 1):
                self.result += 1
                res = 2
                response.append([1, x, y, res])     # only positive response. negative response is updated in visited array
            else:
                res = 1
            self.visited[x][y] = res

        return response

    def identifyBoats(self):

        if(self.result > 15 or self.t <= 0):       # total is 17/100
            return self.result

        response = []
        while(len(response) == 0 and self.t > 0):
            # Lets fire first n random shots.
            while(len(self.pos) < self.n):
                # TODO - ships have more probablity to be in the central area  # 5 x 5
                tem = [0, random.randint(0, 9), random.randint(0, 9)]   
                if(tem not in self.pos and self.visited[tem[1]][tem[2]] == 0):
                    heapq.heappush(self.pos, tem)
            response = self.fireShotsAndUpdateResponse()

        while(t > 0 and len(response) > 0):
            p, x, y, res = response[-1]
            response.pop()

            # explore if we can identify a direction and give it higher priority
            # or else explore with lower priority
            for i in range(4):
                x2, y2 = x + dirx[i], y + diry[i]
                x3, y3 = x + opp_dirx[i], y + opp_diry[i]
                priority = 0        # default
                if(self.isValid(x2, y2) and self.visited[x2][y2] == 0):
                    if(self.isValid(x3, y3)):
                        if self.visited[x3][y3] == 2:        # ship on one side
                            priority = -20               # highest
                        elif self.visited[x3][y3] == 1:      # surely water on one side -- increases chances
                            priority = -10               # middle priority
                        else:                           # unknown on one side
                            priority = -5
                    heapq.heappush(self.pos, [priority, x2, y2])

        return self.identifyBoats()

if __name__ == '__main__':
    
    n = int(input("Enter number of shots allowed at once:   "))
    t = int(input("Enter total number of ammunitions:       "))        # total number of shots

    print("Region provided is: ")
    region = [  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            ]

    my_algo = CodeComp(n, t, region)
    [print(x) for x in my_algo.region]
    print("Boat positions identified : ", my_algo.identifyBoats())

    print("Other important details to the algo::")
    print("Amunition provided:", t, "vs Amunition used:", t - my_algo.t)

    print("Visited matrix looks like: ")
    [print(x) for x in my_algo.visited]
    print("Accuracy :", (my_algo.identifyBoats() / (t - my_algo.t)) * 100)
    print(my_algo.pos)
    print("----------------------------------------------------------------")