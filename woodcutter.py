#! python3

"""
woodcutter.py

Cuts trees and drops the logs
Future improvements:
 - Cutting other types of logs
 - Banking valuable logs (ie yews)
"""

import os, sys, time, logging, math, colorsys, random
import pyautogui as pag
import helpers
import loginInfo
import gui
from PIL import ImageGrab, Image
import win32api, win32con

pag.PAUSE = 0.05
logging.getLogger().setLevel(logging.INFO)


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
            h,trash1,trash2 = colorsys.rgb_to_hsv(val[0], val[1], val[2])
            #may need to change the below if statement;
            #hue tolerance depends on background of text
            if 115 < 240*h < 125:
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
    helpers.mouseTo(pos[0], pos[1])
    return isMouseOnTree()

# Helper function for concentricList
# tlc = top-left corner of rect
# dims = dimensions of rect
# n, m = matrix dimensions
def addSides(posList, tlc, dims, n, m):
    i = tlc[0]
    j = tlc[1]
    L = tlc[0]
    R = tlc[0] + (dims[0]-1)
    U = tlc[1]
    D = tlc[1] + (dims[1]-1)
    while i < R:
        if -1 < i < n and -1 < j < m:
            posList.append((i,j))
        i += 1
    while j < D:
        if -1 < i < n and -1 < j < m:
            posList.append((i,j))
        j += 1
    while i > L:
        if -1 < i < n and -1 < j < m:
            posList.append((i,j))
        i -= 1
    while j > U:
        if -1 < i < n and -1 < j < m:
            posList.append((i,j))
        j -= 1      
        
# List the coordinates of a nxm matrix in
# concentric rectangular rings from the center out    
def concentricList(n, m):
    # Set up central rect ring
    rectX = 0
    rectY = 0
    rectL = 0
    rectH = 0
    if n % 2 == 0:
        rectX = n//2 - 1
        rectL = 2
    else:
        rectX = (n-1)//2
        rectL = 1
    if m % 2 == 0:
        rectY = m//2 - 1
        rectH = 2
    else:
        rectY = (m-1)//2
        rectH = 1

    # Add central rect ring
    posList = []
    cent = ((rectX, rectY),
            (rectX+1,rectY),
            (rectX+1,rectY+1),
            (rectX,rectY+1))
    posList.append(cent[0])
    if n % 2 == 0:
        posList.append(cent[1])
        if m % 2 == 0:
            posList.append(cent[2])
            posList.append(cent[3])
    elif m % 2 == 0:
        posList.append(cent[3])

    # Move outward adding the other rect rings
    while rectX > -1 or rectY > -1:
        rectX -= 1
        rectY -= 1
        rectL += 2
        rectH += 2
        addSides(posList, (rectX, rectY), (rectL, rectH), n, m)

    return posList

# Get hue counts from a patch (of rgba values)
def getHueCounts(patch, patchSize):
    hues = {}
    for i in range(patchSize):
        for j in range(patchSize):
            rgba = patch[i,j]
            rgb = tuple(x/255 for x in rgba[:3])
            hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
            hue = int(round(hls[0]*240))
            if hue in hues:
                hues[hue] += 1
            else:
                hues[hue] = 1
    return hues

# Get hue from an rgb tuple
def getHueFromRgb(rgb):
    rgbPct = tuple(x/255 for x in rgb[:3])
    hue, trash1, trash2 = colorsys.rgb_to_hls(rgbPct[0], rgbPct[1], rgbPct[2])
    return int(round(hue*240))

# Get patch at position, decide if it's probably a tree
def isTreeAtPos(pos, patchSize, treeType):
    im = ImageGrab.grab((pos[0], pos[1], pos[0]+patchSize, pos[1]+patchSize))
    patch = im.load()
    hues = getHueCounts(patch, patchSize)
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

    blockLen = 37
    halfBlock = (blockLen + 1)//2
    positions = concentricList(14,9)
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

    blockLen = 37
    halfBlock = (blockLen + 1)//2
    positions = concentricList(14,9)
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
            helpers.Ox + helpers.stump['tlcX'],
            helpers.Oy + helpers.stump['tlcY'],
            helpers.Ox + helpers.stump['brcX'],
            helpers.Oy + helpers.stump['brcY']
            ))
        sWidth = helpers.stump['width']
        sHeight = helpers.stump['height']
        sRadius = helpers.stump['radius']
    elif treeType == 'Oak':
        im = ImageGrab.grab((
            helpers.Ox + helpers.oakstump['tlcX'],
            helpers.Oy + helpers.oakstump['tlcY'],
            helpers.Ox + helpers.oakstump['brcX'],
            helpers.Oy + helpers.oakstump['brcY']
            ))
        sWidth = helpers.oakstump['width']
        sHeight = helpers.oakstump['height']
        sRadius = helpers.oakstump['radius']
    elif treeType == 'Willow':
        im = ImageGrab.grab((
            helpers.Ox + helpers.willowstump['tlcX'],
            helpers.Oy + helpers.willowstump['tlcY'],
            helpers.Ox + helpers.willowstump['brcX'],
            helpers.Oy + helpers.willowstump['brcY']
            ))
        sWidth = helpers.willowstump['width']
        sHeight = helpers.willowstump['height']
        sRadius = helpers.willowstump['radius']
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
                hue = getHueFromRgb(pix[x,y])
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

### Inventory/HUD --------------------------------------------------------------
# Process text for detecting any inventory item
def processImageInv(im):
    pix = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            val = pix[i,j]
            trash1,s,trash2 = colorsys.rgb_to_hsv(val[0], val[1], val[2])
            if 240*s < 41:
                pix[i,j] = (255,255,255)
            else:
                pix[i,j] = (0,0,0)

# Check if last inventory slot is empty
def isInvSlotEmpty(slot):
    tlc = helpers.hud['invSlotsTlcs'][slot]
    size = helpers.hud['invSlotLen']
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    return pag.locate('images\\emptyinv' + str(slot) + '.png', im)

# Check if item is in inventory slot
def isItemInSlot(name, slot):
    tlc = helpers.hud['invSlotsTlcs'][slot]
    size = helpers.hud['invSlotLen']
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    try:
        itemIm = Image.open('images\\invitem' + name + '.png')
        return pag.locate(itemIm, im)
    except:
        logging.warning('Image for item ' + name + ' not found.')
        return False

# Get first empty inventory slot; return -1 if full
def firstEmptyInvSlot():
    for i in range(28):
        if isInvSlotEmpty(i):
            return i
    return -1

# Get last empty inventory slot from the end
# Explanation: start at end, and move backwards until you reach nonempty slot.
# If return 28, last inv slot is nonempty.
# If return -1, inventory is empty
def endLastEmptyInvSlot():
    for i in range(27,-1,-1):
        if not isInvSlotEmpty(i):
            return (i+1)
    return -1

# Check for full inventory
def isInvFull():
    return (firstEmptyInvSlot() < 0)

# Empty inventory
## Note: must have shift+click dropping enabled
## Also, must have axe equipped or you will drop it!
def dropAllInv():
    pag.keyDown('shift')
    for pos in helpers.hud['invSlots']:
        helpers.mouseTo(pos[0], pos[1])
        pag.click()
    pag.keyUp('shift')

# Empty inventory (except first space - where you should put axe)
## Note: must have shift+click dropping enabled
def dropAllButOneInv():
    pag.keyDown('shift')
    for pos in helpers.hud['invSlots'][1:]:
        helpers.mouseTo(pos[0], pos[1])
        pag.click()
    pag.keyUp('shift')

# Drop all of a certain item
## Note: must have shift+click dropping enabled
def dropAllItem(name):
    pag.keyDown('shift')
    for i in range(28):
        if isItemInSlot(name=name, slot=i):
            pos = helpers.hud['invSlots'][i]
            helpers.mouseTo(pos[0], pos[1])
            pag.click()
    pag.keyUp('shift')

# Click a HUD tab
def clickHudTab(tabName):
    try:
        helpers.clickButton(helper.images[tabName + 'Tab'])
    except:
        return ''
    return tabName

# Click map at given coords (relative to map center)
def clickMap(x, y):
    r = helpers.hud['mapRadius']
    if (x*x + y*y > r*r):
        logging.warning('Invalid position passed to clickMap')
        return
    center = helpers.hud['mapCenter']
    helpers.mouseTo(center[0]+x, center[1]+y)
    time.sleep(0.5)
    pag.click()
        
### Camera/holdKey -------------------------------------------------------------
# Hold a key press
def holdKey(key, holdTime):
    keys = {
        'right': win32con.VK_RIGHT,
        'left': win32con.VK_LEFT,
        'up': win32con.VK_UP,
        'down': win32con.VK_DOWN,
        }
    if key in keys:
        winKey = keys[key]
        win32api.keybd_event(winKey, 0, 0, 0)
        stopTime = time.time() + holdTime
        while time.time() < stopTime:
            win32api.keybd_event(winKey, 0, 0, 0)
            time.sleep(0.01)
        win32api.keybd_event(winKey, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        logging.warning('Unrecognized key passed to holdKey')

# Reset camera to north-facing top-down view
def resetCamera():
    #pag.moveTo(helpers.hud['compass'])
    pos = helpers.hud['compass']
    helpers.mouseTo(pos[0], pos[1])
    pag.click()
    holdKey('up', 2)

# Rotate camera slightly
def perturbCamera():
    holdKey('right', 0.2)

### Misc. ----------------------------------------------------------------------
# Check if under attack by looking for health bar
def isUnderAttack():
    Ox, Oy = helpers.coordsClientToPix((0,0))
    im = ImageGrab.grab((Ox + 222, Oy + 129, Ox + 298, Oy + 181))
    if pag.locate('images\\hbargreen.png', im):
        return True
    if pag.locate('images\\hbarred.png', im):
        return True
    return False

# Run away until not under attack
def evade():
    r = helpers.hud['mapRadius']
    clickMap(0,-r)
    while isUnderAttack():
        logging.info('Under attack')
        if random.randint(0,1):
            clickMap(0,-r) # north
        else:
            clickMap(-r,0) # west
        time.sleep(3)


#-------------------------------------------------------------------------------
"""
Script
"""

# Start client and log in if not already
clientName = loginInfo.clientName
clientPath = loginInfo.clientPath
if not helpers.startClient(clientName, clientPath):
    print('Could not start client. Exiting')
    sys.exit(0)
helpers.login(loginInfo.username, 393)

# Use GUI to get user options, then reformat some options
options = gui.woodcutterStartGui()
if options['start'].get() == 'Cancel':
    print('User cancelled script. Exiting')
    sys.exit(0)
if options['start'].get() == 'Close':
    print('User closed window. Exiting')
    sys.exit(0)
for key in options:
    options[key] = options[key].get()
if options['treetype'] == 'Normal':
    options['invitem'] = 'Logs'
else:
    options['invitem'] = options['treetype'] + ' logs'

# Set up HUD, camera, inventory
helpers.focusClient(clientName)
helpers.setHud()
hudTab = clickHudTab('inventory')
resetCamera()
if isInvFull():
    logging.info('Detected full inventory')
    logging.info('Emptying inventory...')
    dropAllItem(options['invitem'])
    logging.info('Done emptying.')

findNewTree = True
failCounter = 0
blocked = False

## Main loop for finding and chopping trees
while findNewTree:
    
    # Try to find a tree
    logging.info('Searching for tree...')
    if isUnderAttack():
            evade()
    if failCounter > 10:
        print('Failed to find tree. Exiting')
        sys.exit(0)
    if failCounter > 0 and not blocked:
        perturbCamera()
    possibleTrees = findTrees(options['treetype'])
    clickedTree = False
    if blocked:
        # Shuffle possibleTrees so you don't keep clicking the blocked tree
        possibleTrees = random.sample(possibleTrees, len(possibleTrees))
    for pos in possibleTrees:
        helpers.mouseTo(pos[0], pos[1])
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
        resetCamera()
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
    maxSec = random.randint(8, 12) #wait 8-12 sec to fell tree
    logging.info('Waiting to finish chopping...')
    while not newStumpFound:
        scanCounter += 1
        if isUnderAttack():
            evade()
        elif scanCounter > maxSec: #wait no longer than maxSec to fell tree
            break
        elif isItemInSlot(options['invitem'], 27): #check for full inv
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
    if isUnderAttack():
        evade()          
    # If Logs in last inv slot, drop all Logs
    if isItemInSlot(options['invitem'], 27):
        logging.info('Full inventory. Emptying...')
        dropAllItem(options['invitem'])
        logging.info('Done emptying.')

    
    
    


