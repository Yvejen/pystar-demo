#!/usr/bin/env python3
from graphics import *
from heapq import *
from itertools import chain

# Author: Henri Gerigk
# Date:   Mon May 21 22:05:39 CEST 2018
# A* Demo
# A* Algorithm with an editable grid

# This script uses graphics.py written by John Zelle
# http://mcsp.wartburg.edu/zelle/python/

#Window Size
resolution = 600
#Nummber of cells per line/column
grid_res = 20
rec_size = int(resolution/grid_res)


class Node(object):
    def __init__(self,x,y,walkable=True,h=0,g=0,hi=0):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.h = 0
        self.g = 0
        self.closed = False
        self.open   = False
        self.graphObject = Rectangle(Point(x*rec_size,y*rec_size),Point((x+1)*rec_size,(y+1)*rec_size))
    def __lt__(self,other):
        otherf = other.g + other.h
        thisf  = self.g + self.h
        if thisf < otherf:
            return True
        elif thisf == otherf:
            return self.h < other.h
        else:
            return False
    def __eq__(self,other):
            return self.x == other.x and self.y == other.y
    def __hash__(self):
            return self.y*grid_res+self.x

def screenToGrid(p):
    return int(p.getX()/rec_size),int(p.getY()/rec_size)


#Setup Grid
Nodes = [[Node(x,y) for y in range(grid_res)] for x in range(grid_res)]

win = GraphWin("A* Algorithm Demo", resolution, resolution, autoflush=False)
win.setBackground("white")
#Draw all the Nodes
for Node in chain.from_iterable(Nodes): Node.graphObject.draw(win)

start = None
goal  = None

#User defined Grid
setup = True
while setup:
    key = win.checkKey()
    if key == 'q':
        setup=False
    if key == 's':
        p = win.getMouse()
        x,y = screenToGrid(p)
        if start:
            start.graphObject.setFill("white")
        start = Nodes[x][y]
        Nodes[x][y].graphObject.setFill("blue")
    if key == 'l':
        #Load saved grid
        static_grid = [(0, 15), (1, 15), (2, 15), (3, 15), (4, 15), (5, 5), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (6, 5), (6, 8), (7, 5), (7, 8), (8, 5), (8, 8), (9, 5), (9, 8), (9, 10), (9, 11), (10, 5), (10, 8), (10, 12), (11, 5), (11, 8), (11, 12), (12, 5), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (13, 5), (13, 14), (14, 5), (14, 14), (15, 5), (15, 14), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14)]


        start_coord = (6,9)
        goal_coord = (2,10)

        for coord in static_grid:
            Nodes[coord[0]][coord[1]].walkable = False
            Nodes[coord[0]][coord[1]].graphObject.setFill("red")
        start = Nodes[start_coord[0]][start_coord[1]]
        start.graphObject.setFill("blue")
        goal  = Nodes[goal_coord[0]][goal_coord[1]]
        goal.graphObject.setFill("green")
    if key == 'p':
        print ([(Node.x,Node.y) for Node in chain.from_iterable(Nodes) if not Node.walkable])
        print ((start.x,start.y))
        print ((goal.x,goal.y))
    if key == 'g':
        p = win.getMouse()
        x,y = screenToGrid(p)
        if goal:
            goal.graphObject.setFill("white")
        goal = Nodes[x][y]
        Nodes[x][y].graphObject.setFill("green")

    p = win.checkMouse()
    if p:
        x,y = screenToGrid(p)
        Nodes[x][y].walkable = not Nodes[x][y].walkable 
        Nodes[x][y].graphObject.setFill("white" if Nodes[x][y].walkable else "red")

def dist(nod1,nod2):
    return abs(nod1.x - nod2.x) + abs(nod1.y - nod2.y)

def neigh(center):
    #return [node for node in [Nodes[center.x-1][center.y],Nodes[center.x+1][center.y],Nodes[center.x][center.y-1],Nodes[center.x][center.y+1]] if node.walkable]
    coords = [(center.x+c[0],center.y+c[1]) for c in [(-1,0),(1,0),(0,-1),(0,1)] if c[0]+center.x < grid_res and c[1]+center.y < grid_res and c[0]+center.x >= 0 and c[1]+center.y >= 0]
    return [Nodes[c[0]][c[1]] for c in coords if Nodes[c[0]][c[1]].walkable]

#A* algorithm
openHeap = [start]
predecessor = {}
start.g = 0
start.h = dist(start,goal)
start.open = True

while openHeap and win.checkKey() != 'q':
    update(8)
    current = heappop(openHeap)
    if current == goal:
        path = [goal]
        #current = goal
        while path[-1] != start:
            path.append(predecessor[path[-1]])
        for node in path: node.graphObject.setFill("yellow")
        break

    #win.getMouse()

    current.open = False
    current.closed = True
    current.graphObject.setFill("grey")

    for node in neigh(current):
        if node.closed:
            continue
        tentative_g = current.g + dist(current,node)
        if tentative_g >= node.g and node.g != 0:
            continue

        predecessor[node] = current
        node.g = tentative_g
        node.h = dist(node,goal)

        if not node.open:
            node.open = True
            node.graphObject.setFill("cyan")
            heappush(openHeap,node)
        else:
            heapify(openHeap)

win.getKey()
win.close()
