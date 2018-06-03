#! python3

import time
import random
import math
import pyautogui as pag
from mouseMoveLog import records

"""
Mouse move function that uses mouse movements stored in mouseMoveLog
"""

def dot(v1, v2):
    return (v1[0]*v2[0] + v1[1]*v2[1])

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


# Return pair (cosA, sinA) where A is the angle between vectors
def trigsBetween(v1, v2):
    n1 = norm(v1)
    n2 = norm(v2)
    if n1 < 0.00001 or n2 < 0.00001:
        print('Zero vector passed to trigsBetween')
        return False
    orthv1 = (-1*v1[1], v1[0])
    return ( dot(v1, v2) / (n1*n2), dot(orthv1, v2) / (n1*n2) )


# Return angle between vectors
def angleBetween(v1, v2):
    cos, sin = trigsBetween(v1, v2)
    return math.atan2(sin, cos)


# Run a mouse move (list of mouse events)
def runMove(mouseMove):
    # Compute random perturbations
    for i in range(random.randint(0,5)):
        ind = random.randint(1, len(mouseMove)-2)
        pos = mouseMove[ind]['position']
        mouseMove[ind]['position'] = (
            pos[0] + random.randint(-1,1), pos[1] + random.randint(-1,1)
            )
    # Run move
    i = 0
    move = mouseMove[i]
    startTime = time.time()
    while i < len(mouseMove) - 1:
        if time.time() - startTime > move['time']:
            pag.moveTo(move['position'][0], move['position'][1])
            i += 1
            move = mouseMove[i]

# Move mouse to (x2 y2)
def mouseTo(x2, y2):
    
    pause = pag.PAUSE
    pag.PAUSE = 0
    
    x1, y1 = pag.position()
    
    # Pick a random recorded move to use as the basis to compute move
    moveLen = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    if moveLen < 80:
        lenClass = 's'
    elif moveLen < 200:
        lenClass = 'm'
    elif moveLen < 350:
        lenClass = 'l'
    elif moveLen < 500:
        lenClass = 'xl'
    else:
        lenClass = 'xxl'
    moveR = records[lenClass][random.randint(0, len(records[lenClass])-1)]

    # Define function that transforms direction vector of recorded move
    # to direction vector of computed path
    aR = moveR[0]['position']
    bR = moveR[len(moveR) - 1]['position']
    aC = (x1, y1)
    bC = (x2, y2)
    vR = (bR[0] - aR[0], bR[1] - aR[1])
    vC = (bC[0] - aC[0], bC[1] - aC[1])
    cos, sin = trigsBetween(vR, vC)
    def mapRtoC (pos):
        # Translate to origin
        xNew = pos[0] - aR[0]
        yNew = pos[1] - aR[1]
        # Rotate
        xNewTemp = xNew
        xNew = xNew*cos - yNew*sin
        yNew = xNewTemp*sin + yNew*cos
        # Scale
        rat = norm(vC) / norm(vR)
        xNew *= rat
        yNew *= rat
        # Translate to aC
        xNew += aC[0]
        yNew += aC[1]
        return (xNew, yNew)

    # Transform recorded move using new function, then run
    move = []
    for i in range(len(moveR)):
        evt = moveR[i]
        move.append({
            'position': mapRtoC(evt['position']),
            'time': evt['time']
            })
    runMove(move)

    pag.PAUSE = pause
    


    
