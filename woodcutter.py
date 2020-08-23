#! python3

"""
woodcutter.py

Cuts trees and drops the logs
Future improvements:
 - Banking valuable logs (ie yews)
"""

import os
import sys
import time
import logging
import math
import random
import pyautogui as pag
import helpers
import loginInfo
import gui
from mouseMoveFunction import mouseTo
from PIL import ImageGrab
from PIL import Image

pag.PAUSE = 0.05
logging.getLogger().setLevel(logging.INFO)


"""
Variables
"""
# Stump-finding constants
stump = {
    'tlcX': 211,
    'tlcY': 128,
    'brcX': 309,
    'brcY': 221,
    'radius': 17,
    }
stump['width'] = stump['brcX'] - stump['tlcX']
stump['height'] = stump['brcY'] - stump['tlcY']
oakstump = {
    'tlcX': 188,
    'tlcY': 99,
    'brcX': 324,
    'brcY': 235,
    'radius': 38,
    }
oakstump['width'] = oakstump['brcX'] - oakstump['tlcX']
oakstump['height'] = oakstump['brcY'] - oakstump['tlcY']
willowstump = {
    'tlcX': 208,
    'tlcY': 119,
    'brcX': 324,
    'brcY': 235,
    'radius': 38,
    }
willowstump['width'] = willowstump['brcX'] - willowstump['tlcX']
willowstump['height'] = willowstump['brcY'] - willowstump['tlcY']


"""
Functions
"""
### Tree/Stump Finding ---------------------------------------------------------
# Process image into white text on black bg
# For detecting 'Tree'
def processImageTree(im):
    pix = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            val = pix[i,j]
            h = helpers.getHueFromRgb((val[0], val[1], val[2]))
            #may need to change the below if statement;
            #hue tolerance depends on background of text
            if 115 < h < 125:
                pix[i,j] = (255,255,255)
            else:
                pix[i,j] = (0,0,0)

# Screenshot and process shot to search cursor text for tree name
# This should have no false positives
def isMouseOnTree(treeType):
    pixCd1 = helpers.coordsClientToPix((81,7))
    pixCd2 = helpers.coordsClientToPix((115,21))
    im = ImageGrab.grab((pixCd1[0], pixCd1[1], pixCd2[0], pixCd2[1]))
    processImageTree(im)
    treeFound = False
    if treeType == 'Normal':
        pathPre = 'images\\testTree'
        nPics = 6
    elif treeType == 'Oak':
        pathPre = 'images\\testOak'
        nPics = 3
    elif treeType == 'Willow':
        pathPre = 'images\\testWillow'
        nPics = 4
    for i in range(nPics):
        if pag.locate(pathPre + str(i+1) + '.png', im):
            return True
    return False

# Determine if tree is at given position
def isTreeAtPosition_old(pos):
    mouseTo(pos[0], pos[1])
    return isMouseOnTree()

# Get patch at position, decide if it's probably a tree
def isTreeAtPos(pos, patchSize, treeType):
    im = ImageGrab.grab((pos[0], pos[1], pos[0]+patchSize, pos[1]+patchSize))
    patch = im.load()
    hues = helpers.getHueCounts(patch, patchSize)
    rankedHues = sorted(hues, key=hues.get, reverse=True)
    if not 48 in rankedHues[:3]:
        return False
    inRangeCount = 0
    for hue in range(46, 50):
        if hue in hues:
            inRangeCount += hues[hue]
    if treeType == 'Normal' or treeType == 'Oak':
        if ( inRangeCount/(patchSize*patchSize) < 0.25 ):
            return False
        if ( not 40 in hues ) or ( hues[40]/(patchSize*patchSize) < 0.025 ):
            return False
        return True
    if treeType == 'Willow':
        if ( inRangeCount/(patchSize*patchSize) < 0.25 ):
            return False
        if ( not 44 in hues ) or ( hues[44]/(patchSize*patchSize) < 0.025 ):
            return False
        return True

# Return a list of probable positions with trees based on sampling
# pixel patches
# Positions might not actually be trees.
def findTrees(treeType):
    pixCd1 = helpers.coordsClientToPix((4,4))
    pixCd2 = helpers.coordsClientToPix((516,338))
    im = ImageGrab.grab((pixCd1[0], pixCd1[1], pixCd2[0], pixCd2[1]))

    blockLen = helpers.viewBlockLen
    halfBlock = (blockLen + 1)//2
    positions = helpers.viewPositions
    patchSize = 8
    halfPatch = patchSize//2
    goodPositions = []
    
    for i in range(len(positions)):
        x = blockLen*positions[i][0] + halfBlock
        y = blockLen*positions[i][1] + halfBlock
        pos = helpers.coordsClientToPix((x,y))
        if isTreeAtPos(pos, patchSize, treeType):
            goodPositions.append((pos[0] + halfPatch, pos[1] + halfPatch))
            
    return goodPositions

# Return at most n positions
def findNTrees_old(n):
    pixCd1 = helpers.coordsClientToPix((4,4))
    pixCd2 = helpers.coordsClientToPix((515,341))
    im = ImageGrab.grab((pixCd1[0], pixCd1[1], pixCd2[0], pixCd2[1]))

    blockLen = helpers.viewBlockLen
    halfBlock = (blockLen + 1)//2
    positions = helpers.viewPositions
    goodPositions = []
    for i in range(len(positions)):
        x = blockLen*positions[i][0] + halfBlock
        y = blockLen*positions[i][1] + halfBlock
        pos = helpers.coordsClientToPix((x,y))
        if isTreeAtPosition(pos):
            goodPositions.append(pos)
            if len(goodPositions) == n:
                break
    return goodPositions

# Return a single position with a tree (close to player).
def findOneTree_old():
    pixCd1 = helpers.coordsClientToPix((4,4))
    pixCd2 = helpers.coordsClientToPix((515,341))
    im = ImageGrab.grab((pixCd1[0], pixCd1[1], pixCd2[0], pixCd2[1]))

    blockLen = 37
    halfBlock = (blockLen + 1)//2
    positions = concentricList(14,9)
    for i in range(len(positions)):
        x = blockLen*positions[i][0] + halfBlock
        y = blockLen*positions[i][1] + halfBlock
        pos = helpers.coordsClientToPix((x,y))
        if isTreeAtPosition(pos):
            return pos

# Return a dict with entries 'code':bool where 'code' is a section code
# and the bool indicates if there is a stump in that section
def scanSections(treeType):
    if treeType == 'Normal':
        im = ImageGrab.grab((
            helpers.Ox + stump['tlcX'],
            helpers.Oy + stump['tlcY'],
            helpers.Ox + stump['brcX'],
            helpers.Oy + stump['brcY']
            ))
        sWidth = stump['width']
        sHeight = stump['height']
        sRadius = stump['radius']
    elif treeType == 'Oak':
        im = ImageGrab.grab((
            helpers.Ox + oakstump['tlcX'],
            helpers.Oy + oakstump['tlcY'],
            helpers.Ox + oakstump['brcX'],
            helpers.Oy + oakstump['brcY']
            ))
        sWidth = oakstump['width']
        sHeight = oakstump['height']
        sRadius = oakstump['radius']
    elif treeType == 'Willow':
        im = ImageGrab.grab((
            helpers.Ox + willowstump['tlcX'],
            helpers.Oy + willowstump['tlcY'],
            helpers.Ox + willowstump['brcX'],
            helpers.Oy + willowstump['brcY']
            ))
        sWidth = willowstump['width']
        sHeight = willowstump['height']
        sRadius = willowstump['radius']
    else:
        logging.warning('Invalid treeType in scanSections')
        return -1
        
    pix = im.load()
    hue = 0
    sections = {}
    sectionRanges = {
        'TL': {'x': (0, sWidth//2), 'y': (0, sRadius)},
        'TR': {'x': (sWidth//2, sWidth), 'y': (0, sRadius)},
        'R':  {'x': (sWidth-sRadius, sWidth), 'y': (sRadius, sHeight-sRadius)},
        'BR': {'x': (sWidth//2, sWidth), 'y': (sHeight-sRadius, sRadius)},
        'BL': {'x': (0, sWidth//2), 'y': (sHeight-sRadius, sHeight)},
        'L':  {'x': (0, sRadius), 'y': (sRadius, sHeight-sRadius)},
        }
    # Special center section for willows due to odd tree shape
    if treeType == 'Willow':
        sectionRanges['C'] = {
            'x': (sRadius, sWidth-sRadius), 'y': (sRadius, sHeight-sRadius)
            }
    
    for key in sectionRanges:
        hueCount20 = 0
        hueCount21 = 0
        hueCount22 = 0
        hueCount23 = 0
        hueCount32 = 0
        hueCount38 = 0
        hueCount40 = 0
        for x in range(sectionRanges[key]['x'][0], sectionRanges[key]['x'][1]):
            for y in range(sectionRanges[key]['y'][0], sectionRanges[key]['y'][1]):
                hue = helpers.getHueFromRgb(pix[x,y])
                if hue == 20:
                    hueCount20 += 1
                elif hue == 21:
                    hueCount21 += 1
                elif hue == 22:
                    hueCount22 += 1
                elif hue == 23:
                    hueCount23 += 1
                elif hue == 32:
                    hueCount32 += 1
                elif hue == 38:
                    hueCount38 += 1
                elif hue == 40:
                    hueCount40 += 1
        normalCrit = ( (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3) )
        oakCrit = ( hueCount22 > 60 and hueCount21 > 10 and hueCount23 > 0 )
        willowCrit = (
            hueCount32 < 140 and hueCount32 > 40 and
            (hueCount21 > 2 or (hueCount38 > 3 and hueCount40 < 28))
            )
        if treeType == 'Normal' and normalCrit:
            sections[key] = True
        elif treeType == 'Oak' and oakCrit:
            sections[key] = True
        elif treeType == 'Willow' and willowCrit:
            sections[key] = True
        else:
            sections[key] = False
    return sections


# Cut one log from a tree. Used in tutorial.py
def cutOneLog(treeType, searchTimeLimit=30, tutorial=False):
    # Get empty inv slot and inv item name to search for
    checkSlot = helpers.firstEmptyInvSlot()
    if checkSlot < 0:
        logging.info('Full inventory in cutOneLog')
        return False
    if treeType == 'Normal':
        if tutorial:
            itemName = 'Logs (tutorial)'
        else:
            itemName = 'Logs'
    else:
        itemName = treetype + ' logs'
    logging.info('Searching for ' + itemName + ' in slot ' + str(checkSlot))

    # Loop trying to cut tree until inv slot has a log in it
    while True:
        # Locate and click tree
        clickedTree = False
        start = time.time()
        while time.time() - start < searchTimeLimit:
            positions = findTrees(treeType)
            for pos in positions:
                mouseTo(pos[0], pos[1])
                time.sleep( random.uniform(0.1, 0.15) )
                if isMouseOnTree(treeType):
                    clickedTree = True
                    pag.click()
                    break
            if clickedTree:
                break
            helpers.perturbCamera()
        if not clickedTree:
            logging.info('Failed to find tree after '
                         + str(searchTimeLimit) + ' seconds')
            return False
        
        # Wait until log in inv slot or chop time expires
        start = time.time()
        while time.time() - start < 15:
            if helpers.isItemInSlot(itemName, checkSlot):
                logging.info('Found ' + itemName + '; returning')
                return True
            time.sleep(1)
            
        logging.info(itemName + ' not found in slot ' + str(checkSlot))
        return False


# blockProcess function for stone staircase in Lumbridge Castle
def processStoneStaircase(xBounds, yBounds, pix):
    blue = 0
    pink = 0
    cyan = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 22:
                blue += 1
            elif hue == 21:
                pink += 1
            elif hue == 23:
                cyan += 1
        if blue > 10 and pink > 10 and cyan > 40:
            return True
    return False


# Ascend both stone stairs in south Lumb castle and run to bank
def ascendLumbStairs():
    ax, ay = helpers.coordsClientToPix( helpers.coordConsts['viewTlc'] )
    bx, by = helpers.coordsClientToPix( helpers.coordConsts['viewBrc'] )
    xd = bx - ax
    yd = by - ay
    bbox1 = (ax, ay + yd/2, bx, by)
    bbox2 = (ax + xd/3, ay + yd/2, bx - xd/3, by - yd/4)
    
    if not helpers.clickEntityDialog(
            bbox=bbox1,
            blockProcess=processStoneStaircase,
            option='Climb-up',
            blockDimensions=(40,40),
            name='Staircase'
            ):
        logging.info('Failed to locate stone staircase in Lumb Castle')
        return False
    time.sleep( random.uniform(8, 8.1) )
    if not helpers.clickEntityDialog(
            bbox=bbox1,
            blockProcess=processStoneStaircase,
            option='Climb-up',
            blockDimensions=(40,40),
            name='Staircase'
            ):
        logging.info('Failed to locate stone staircase in Lumb Castle')
        return False
    time.sleep( random.uniform(3.5, 3.6) )
    helpers.clickMap(12, -45)
    time.sleep( random.uniform(7, 7.1) )


# From Lumb castle bank, run to and descend both stone staircases
def descendLumbStairs():
    ax, ay = helpers.coordsClientToPix( helpers.coordConsts['viewTlc'] )
    bx, by = helpers.coordsClientToPix( helpers.coordConsts['viewBrc'] )
    xd = bx - ax
    yd = by - ay
    bbox1 = (ax, ay + yd/2, bx, by)
    bbox2 = (ax + xd/3, ay + yd/2, bx - xd/3, by - yd/4)

    helpers.clickMap(-12, 45)
    time.sleep( random.uniform(7, 7.1) )
    if not helpers.clickEntityDialog(
            bbox=bbox2,
            blockProcess=processStoneStaircase,
            option='Climb-down',
            blockDimensions=(30,30),
            name='Staircase'
            ):
        logging.info('Failed to locate stone staircase in Lumb Castle')
        return False
    time.sleep( random.uniform(3.5, 3.6) )
    if not helpers.clickEntityDialog(
            bbox=bbox2,
            blockProcess=processStoneStaircase,
            option='Climb-down',
            blockDimensions=(40,40),
            name='Staircase'
            ):
        logging.info('Failed to locate stone staircase in Lumb Castle')
        return False
    time.sleep( random.uniform(3.5, 3.6) )
    return True


# Run from lumbridge castle northwest corner to bank
def runLumbCastleNWtoBank():
    # Run to preset starting point
    if helpers.clickMapImage(
            refImage='images\\wc_comprefLCcorner.png',
            timeLimit=15,
            center=False):
        time.sleep( random.uniform(9, 9.1) )
    elif helpers.clickMapImage(
            refImage='images\\wc_comprefLStoreWall.png',
            timeLimit=15 ):
        time.sleep( random.uniform(9, 9.1) )
        helpers.clickMap(-32, 17)
        time.sleep( random.uniform(7, 7.1) )
    else:
        logging.info('Failed to locate Castle NW corner ref points')
        return False

    # Run to staircase
    helpers.clickMapDirection('sw', 0.7)
    time.sleep( random.uniform(5.5, 5.6) )
    helpers.clickMapDirection('s', 0.9)
    time.sleep( random.uniform(7.5, 7.6) )
    helpers.clickMapDirection('se', 0.77)
    time.sleep( random.uniform(7.5, 7.6) )

    # Move up staircases and to bank
    ascendLumbStairs()
    return True


# Based on tree type, run to the appropriate bank
def runToBank(treetype):
    logging.info('Starting run to bank')
    helpers.setRun('on')
    if treetype == 'Oak': 
        # Oaks are close to Lumb castle NW corner, so start there
        runLumbCastleNWtoBank()
    elif treetype == 'Willow':
        # Get near to checkpoint (Lumb castle NW corner)
        helpers.runSeries(['s', 'se', 'se'])
        # Finish rest of bank run
        runLumbCastleNWtoBank()
        return
    elif treetype == 'Yew':
        ###---- TODO ----###
        return
    else:
        logging.info('Invalid treetype: ' + treetype + ' in runToBank')


# Run from bank to woodcutting spot
def runToSpot(treetype):
    if treetype == 'Oak':
        descendLumbStairs()
        time.sleep( random.uniform(1.5, 1.6) )
        helpers.clickMapDirection('nw')
        time.sleep( random.uniform(9, 9.1) )
        helpers.clickMapDirection('n')
        time.sleep( random.uniform(7, 7.1) )
        helpers.clickMapDirection('ne', 0.8)
        time.sleep( random.uniform(4, 4.1) )
    elif treetype == 'Willow':
        descendLumbStairs()
        time.sleep( random.uniform(1.5, 1.6) )
        helpers.clickMapDirection('nw')
        time.sleep( random.uniform(9, 9.1) )
        helpers.runSeries(['n', 'nw', 'n'])
        helpers.clickMapDirection('nw', 0.7)
        time.sleep( random.uniform(5, 5.1) )
        helpers.clickMapDirection('n', 0.3)
        time.sleep( random.uniform(6, 6.1) )
    elif treetype == 'Yew':
        ###---- TODO ----###
        return
    else:
        logging.info('Invalid treetype: ' + treetype + ' in runToSpot')



#-------------------------------------------------------------------------------
"""
Script
"""

# Possible returns:
# 'Cancel' - user cancelled script
# ---
# options format:
# { 'treetype': 'Normal', 'Oak', or 'Willow', 'bank': bool }
# endOptions format:
# { 'condition': 'full' or 'num', 'data': <value> }
# ---
# If banking, should start woodcutter in the correct location for chopping
# or at the correct bank for depositing.
# ---
# Correct chopping locations/banks:
# Normal logs : not implemented
# Oak logs    : 2 oaks west of lumbridge castle/lumbridge castle bank
# Willow logs : 2 willows east of lake near lumb castle/lumb castle bank
# Yew logs    : not implemented yet (trees S edgeville or W castle)

def woodcutter(options=None, clientName=None, endOptions=None):
    logging.info('Starting woodcutter with options = ')
    logging.info(str(options))
    if endOptions:
        logging.info(str(endOptions))
    
    # Get user's client name if not passed to function
    if not clientName:
        clientName = pag.prompt(
            text='Enter client name:',
            default='Old School RuneScape')
        if not clientName:
            print('User cancelled script. Exiting')
            return 'Cancel'
    
    # Use GUI to get user options, then reformat some options
    if not options:
        options = gui.woodcutterStartGui()
        if options['start'].get() == 'Cancel':
            print('User cancelled script. Exiting')
            return 'Cancel'
        if options['start'].get() == 'Close':
            print('User closed window. Exiting')
            return 'Cancel'
        for key in options:
            options[key] = options[key].get()
    
    if options['treetype'] == 'Normal':
        options['invitem'] = 'Logs'
    else:
        options['invitem'] = options['treetype'] + ' logs'
        
    if not 'bank' in options:
        options['bank'] = False

    # Set up HUD, camera, inventory
    helpers.focusClient(clientName)
    helpers.setHud()
    helpers.clickHud('tab_inventory')
    helpers.resetCamera()
    if helpers.firstEmptyInvSlot() < 0:
        logging.info('Inventory is full')
        if endOptions['condition'] == 'full':
            return
        if helpers.isItemInSlot(options['invitem'], 27):
            logging.info('Dropping last item (log)')
            helpers.dropSlot(27)

    # Set up logs counter
    numLogSlots = 0
    logsChopped = 0
    for i in range(28):
        if helpers.isItemInSlot(options['invitem'], i):
            numLogSlots += 1
            logsChopped -= 1 #logsChopped starts negative; counter is updated
                             #after full inventory chopped, so it works out
        elif helpers.isInvSlotEmpty(i):
            numLogSlots += 1        

    # Treefinding vars
    failCounter = 0
    blocked = False

    # Afk/logout timing vars
    enableAfk = True
    afkTimeStart = None
    afkDuration = 0
    isAfk = False
    enableLogout = True
    logoutTimeStart = None
    logoutDuration = 0
    isLogout = False

    ## Main loop
    while True:

        # Check for under attack, afk, or logged out
        if helpers.isUnderAttack():
            helpers.evade()
        if isAfk:
            if time.time() - afkTimeStart > afkDuration:
                isAfk = False
                logging.info('AFK stop')
            else:
                time.sleep(1)
                continue
        # Decide if going afk or logging out
        if not isAfk:
            if random.random() < 0.05:
                isAfk = True
                afkTimeStart = time.time()
                afkDuration = random.randint(3,8)
                logging.info(
                    'AFK start, duration: ' + str(afkDuration) + ' seconds'
                    )
                continue
                
        # Try to find a tree
        logging.info('Searching for tree...')
        if failCounter > 10:
            print('Failed to find tree. Exiting')
            sys.exit(0)
        if failCounter > 0 and not blocked:
            helpers.perturbCamera()
        possibleTrees = findTrees(options['treetype'])
        clickedTree = False
        if blocked:
            # Shuffle possibleTrees so you don't keep clicking the blocked tree
            possibleTrees = random.sample(possibleTrees, len(possibleTrees))
        for pos in possibleTrees:
            mouseTo(pos[0], pos[1])
            time.sleep(0.1)
            if isMouseOnTree(options['treetype']):
                clickedTree = True
                pag.click()
                logging.info('Clicked tree')
                break
        if not clickedTree:
            failCounter += 1
            continue
            
        # Reset camera if moved during treefinding
        if failCounter > 0 and not blocked:
            helpers.resetCamera()
        # Wait to run to tree if cutting Normal trees
        if options['treetype'] == 'Normal':
            time.sleep(2)

        # Check for path blocked text in chat box
        tlc = helpers.coordsClientToPix((9,443))
        brc = helpers.coordsClientToPix((109,454))
        im = ImageGrab.grab((tlc[0], tlc[1], brc[0], brc[1]))
        if pag.locate('images\\blocked.png', im):
            logging.info('Path to tree blocked; choosing again')
            blocked = True
            failCounter += 1
            continue 
        # If started chopping, reset failCounter and blocked
        blocked = False
        failCounter = 0

        # Wait until woodcutting stopped
        # Uses scanSections to detect if new stumps appear near player
        sectionsStart = scanSections(options['treetype'])
        sectionsUpdate = sectionsStart.copy()
        newStumpFound = False
        scanCounter = 0
        ### Note: can use dif val of maxSec to optimize for dif trees/locs
        maxSec = random.randint(8, 12) #wait 8-12 sec to fell tree
        logging.info('Waiting to finish chopping...')
        while not newStumpFound:
            scanCounter += 1
            if helpers.isUnderAttack():
                helpers.evade()
            elif scanCounter > maxSec: #wait no longer than maxSec to fell tree
                break
            elif helpers.isItemInSlot(options['invitem'], 27): #check full inv
                break
            else:
                time.sleep(1)
                sectionsUpdate = scanSections(options['treetype'])
                for sec in sectionsStart:
                    if sectionsStart[sec] == False and sectionsUpdate[sec] == True:
                        newStumpFound = True
                        break
        # Exited loop: log reason
        if newStumpFound:
            logging.info('Finished chopping tree.')
        elif scanCounter > maxSec:
            logging.info('Chopping time expired.')
        else:
            logging.info('Ran out of inventory space.')
                         
        # If under attack, evade
        if helpers.isUnderAttack():
            helpers.evade()          
        # Handle full inventory
        if helpers.isItemInSlot(options['invitem'], 27):
            logsChopped += numLogSlots
            if options['bank']: # If banking logs...
                # Run to bank
                runToBank(options['treetype'])
                # Deposit logs
                slot = helpers.searchInv(options['invitem'], numbered=False)
                helpers.openBankInterface()
                helpers.invDialog('deposit-all', slot=slot, numbered=False)
                time.sleep( random.uniform(0.05, 0.15) )
                helpers.clickButton('images\\closeviewbutton.png')
                # End wc if end condition satisfied
                if endOptions['condition'] == 'full':
                    return {'end': 'full', 'data': logsChopped}
                logging.info('Deposited ' + str(logsChopped) + ' logs')
                if (endOptions['condition'] == 'num' and
                        logsChopped >= endOptions['data']):
                    return {'end': 'num', 'data': logsChopped}
                # Run back
                runToSpot(options['treetype'])
            else: # If not banking logs...
                if endOptions['condition'] == 'full':
                    return {'end': 'full', 'data': logsChopped}
                logging.info('Chopped ' + str(logsChopped) + ' logs')
                if (endOptions['condition'] == 'num' and
                        logsChopped >= endOptions['data']):
                    return {'end': 'num', 'data': logsChopped}
                logging.info('Full inventory. Emptying...')
                helpers.dropAllItem(options['invitem'])
                logging.info('Done emptying.')

    
    
    


