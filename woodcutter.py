#! python3

"""
woodcutter.py

Cuts normal trees and drops the logs
"""

import os, sys, time, logging, math, colorsys, random
import pyautogui as pag
import helpers
import loginInfo
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

# Screenshot and process shot to search text and find 'Tree'
# This should have no false positives.
def isMouseOnTree():
    pixCd1 = helpers.coordsClientToPix((81,7))
    pixCd2 = helpers.coordsClientToPix((115,21))
    im = ImageGrab.grab((pixCd1[0], pixCd1[1], pixCd2[0], pixCd2[1]))
    processImageTree(im)
    for i in range(6):
        if pag.locate('images\\testTree' + str(i+1) + '.png', im):
            return True
    return False

# Determine if tree is at given position
def isTreeAtPosition_old(pos):
    #pag.moveTo(pos[0], pos[1], 0.1)
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
def isTreeAtPos(pos, patchSize):
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
    if ( inRangeCount/(patchSize*patchSize) < 0.25 ):
        return False
    if ( not 40 in hues ) or ( hues[40]/(patchSize*patchSize) < 0.025 ):
        return False
    return True

# Return a list of probable positions with trees based on sampling
# pixel patches
# Positions might not actually be trees.
def findTrees():
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
        if isTreeAtPos(pos, patchSize):
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
def scanSections():
    im = ImageGrab.grab((
        helpers.Ox + helpers.stump['tlcX'],
        helpers.Oy + helpers.stump['tlcY'],
        helpers.Ox + helpers.stump['brcX'],
        helpers.Oy + helpers.stump['brcY']
        ))
    pix = im.load()
    sWidth = helpers.stump['width']
    sHeight = helpers.stump['height']
    sRadius = helpers.stump['radius']

    sections = {}
    
    # TL
    hueCount20 = 0
    hueCount21 = 0
    for x in range(0, sWidth//2):
        for y in range(sRadius):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['TL'] = True
    else:
        sections['TL'] = False
        
    # TR
    hueCount20 = 0
    hueCount21 = 0
    for x in range(sWidth//2, sWidth):
        for y in range(sRadius):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['TR'] = True
    else:
        sections['TR'] = False
        
    # R
    hueCount20 = 0
    hueCount21 = 0
    for x in range(sWidth - sRadius, sWidth):
        for y in range(sRadius, sHeight - sRadius):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['R'] = True
    else:
        sections['R'] = False
        
    # BR
    hueCount20 = 0
    hueCount21 = 0
    for x in range(sWidth//2, sWidth):
        for y in range(sHeight - sRadius, sHeight):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['BR'] = True
    else:
        sections['BR'] = False
        
    # BL
    hueCount20 = 0
    hueCount21 = 0
    for x in range(0, sWidth//2):
        for y in range(sHeight - sRadius, sHeight):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['BL'] = True
    else:
        sections['BL'] = False
        
    # L
    hueCount20 = 0
    hueCount21 = 0
    for x in range(sRadius):
        for y in range(sRadius, sHeight - sRadius):
            if getHueFromRgb(pix[x,y]) == 20:
                hueCount20 += 1
            elif getHueFromRgb(pix[x,y]) == 21:
                hueCount21 += 1
    if (hueCount20 > 1) or (hueCount20 > 0 and hueCount21 > 3):
        sections['L'] = True
    else:
        sections['L'] = False
    # Return result
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
        #pag.moveTo(pos[0], pos[1], 0.1)
        helpers.mouseTo(pos[0], pos[1])
        pag.click()
    pag.keyUp('shift')

# Empty inventory (except first space - where you should put axe)
## Note: must have shift+click dropping enabled
def dropAllButOneInv():
    pag.keyDown('shift')
    for pos in helpers.hud['invSlots'][1:]:
        #pag.moveTo(pos[0], pos[1], 0.1)
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
            #pag.moveTo(pos[0], pos[1], 0.1)
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
    #pag.moveTo(center[0]+x, center[1]+y, 0.1)
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
clientName = 'RuneLite'
clientPath = 'C:\\RuneLite\\RuneLite.exe'
if not helpers.startClient(clientName, clientPath):
    print('Could not start client. Exiting')
    sys.exit(0)
helpers.login(loginInfo.username, 393)

# Ask user to start script
userConfirm = pag.confirm(
    text='Click OK to start woodcutting script',
    title='Woodcutting',
    buttons=['OK', 'Cancel']
    )
if userConfirm == 'Cancel':
    print('User cancelled script. Exiting')
    sys.exit(0)
helpers.focusClient(clientName)
helpers.setHud()

# Set up HUD, camera, inventory
hudTab = clickHudTab('inventory')
resetCamera()
if isInvFull():
    logging.info('Detected full inventory')
    logging.info('Emptying inventory...')
    dropAllInv()
    logging.info('Done emptying.')

findNewTree = True
failCounter = 0
blocked = False
while findNewTree:
    
    # Try to find a tree
    logging.info('Searching for tree...')
    if failCounter > 5:
        print('Failed to find tree. Exiting')
        sys.exit(0)
    if failCounter > 0 and not blocked:
        perturbCamera()
    possibleTrees = findTrees()
    clickedTree = False
    if blocked:
        possibleTrees = random.sample(possibleTrees, len(possibleTrees))
    for pos in possibleTrees:
        #pag.moveTo(pos[0], pos[1], 0.1)
        helpers.mouseTo(pos[0], pos[1])
        time.sleep(0.1)
        if isMouseOnTree():
            clickedTree = True
            pag.click()
            logging.info('Clicked tree')
            break
    if not clickedTree:
        failCounter += 1
        continue
        
    # Reset camera if moved during treefinding
    # Then wait while you run to tree
    if failCounter > 0 and not blocked:
        resetCamera()
    ##
    ## Note: increasing this time will prevent you from starting a new tree
    ## search while still chopping, but will also cause you to wait the full
    ## 10 seconds if you fell the tree too fast. The former error is preferable
    ## because you'll probably click the tree you're already chopping.
    ##
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
    sectionsStart = scanSections()
    sectionsUpdate = sectionsStart.copy()
    sectionsEqual = True
    scanCounter = 0
    logging.info('Waiting to finish chopping...')
    while sectionsEqual:
        scanCounter += 1
        if isUnderAttack():
            evade()
        elif scanCounter > 10: #will wait no longer than 10 sec to fell tree
            break
        else:
            time.sleep(1)
            sectionsUpdate = scanSections()
            for sec in sectionsStart:
                if sectionsStart[sec] != sectionsUpdate[sec]:
                    sectionsEqual = False
                    break            
    if sectionsEqual:
        logging.info('Chopping time expired.')
    else:
        logging.info('Finished chopping tree.')
                     
    # Chopping has stopped
    # If under attack, evade
    if isUnderAttack():
        evade()          
    # If Logs in last inv slot, drop all Logs
    if isItemInSlot('Logs', 27):
        logging.info('Full inventory. Emptying...')
        dropAllItem('Logs')
        logging.info('Done emptying.')

    
    
    


