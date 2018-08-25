#! python3

"""
helpers.py

Contains general functions and variables used by
multiple different scripts.
"""

import os
import time
import sys
import logging
import random
import math
import colorsys
import pprint
import glob
import pywinauto
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
from pywinauto.application import Application
import pyautogui as pag
from PIL import ImageGrab
from PIL import Image
import win32api
import win32con
from mouseMoveFunction import mouseTo
from private_accounts import accounts
import geSearchCharPatterns as gescp


"""
Variables
"""
# Bank of images

###  For pyinstaller: (not sure if this is necessary... the executable
###  seems to work using just 'images')
#imagesDirPath = os.path.join(os.path.dirname(sys.executable), 'images')
###  For running as python file:
imagesDirPath = 'images'
images = {
    'exbutton': os.path.join(imagesDirPath, 'existinguserbutton.png'),
    'switchbutton': os.path.join(imagesDirPath, 'clicktoswitchbutton.png'),
    '301': os.path.join(imagesDirPath, 'world301button.png'),
    '308': os.path.join(imagesDirPath, 'world308button.png'),
    '316': os.path.join(imagesDirPath, 'world316button.png'),
    '326': os.path.join(imagesDirPath, 'world326button.png'),
    '335': os.path.join(imagesDirPath, 'world335button.png'),
    '371': os.path.join(imagesDirPath, 'world371button.png'),
    '393': os.path.join(imagesDirPath, 'world393button.png'),
    '394': os.path.join(imagesDirPath, 'world394button.png'),
    'loginfield': os.path.join(imagesDirPath, 'loginfield.png'),
    'loginbutton': os.path.join(imagesDirPath, 'loginbutton.png'),
    'playbutton': os.path.join(imagesDirPath, 'clickheretoplaybutton.png'),
    'origin': os.path.join(imagesDirPath, 'origin.png'),
    'equipmentTab': os.path.join(imagesDirPath, 'equipment.png'),
    'inventoryTab': os.path.join(imagesDirPath, 'inventory.png'),
    'logoutTab': os.path.join(imagesDirPath, 'logouttab.png'),
    'logoutbutton': os.path.join(imagesDirPath, 'logoutbutton.png'),
    'signupbutton': os.path.join(imagesDirPath, 'signupbutton.png'),
    'signupbutton2': os.path.join(imagesDirPath, 'signupbutton2.png'),
    'createaccount': os.path.join(imagesDirPath, 'signupwithyouremail.png'),
    'captchabox': os.path.join(imagesDirPath, 'captchabox.png'),
    'submitcreate': os.path.join(imagesDirPath, 'playnowbutton.png'),
    'confirmcreate': os.path.join(imagesDirPath, 'confirmcreate.png'),
    'hbarred': os.path.join(imagesDirPath, 'hbarred.png'),
    'hbargreen': os.path.join(imagesDirPath, 'hbargreen.png'),
}

# List of f2p worlds
f2pWorlds = ['301','308','316','326','335','393','394']

# Origin of coord system relative to client window
# These are intialized in the startClient call
Ox = None
Oy = None

# HUD coords (relative to origin)
hudCoords = {
    'compass': (561, 20),
    'xp': (529, 34),
    'run': (567, 124),
    'tab_combat': (542, 186),
    'tab_skills': (576, 185),
    'tab_quest': (609, 185),
    'tab_inventory': (644, 185),
    'tab_equipment': (675, 184),
    'tab_prayer': (708, 185),
    'tab_magic': (742, 185),
    'tab_clan': (541, 482),
    'tab_friends': (576, 484),
    'tab_ignore': (608, 484),
    'tab_logout': (642, 485),
    'tab_settings': (675, 484),
    'tab_emotes': (710, 483),
    'tab_music': (742, 483),
    'tab_combat_auto': (624, 382),
    'tab_equipment_stats': (573, 432),
    'tab_logout_world': (638, 388),
    'tab_logout_button': (630, 430),
    'tab_settings_display': (573, 225),
    'tab_settings_audio': (619, 225),
    'tab_settings_chat': (662, 226),
    'tab_settings_controls': (709, 226),
    'tab_settings_run': (618, 443),
    'tab_settings_audio_music_0': (610, 287),
    'tab_settings_audio_effect_1': (636, 336),
    'tab_settings_audio_area_1': (635, 383),
    'tab_settings_display_zoom1': (609, 272),
    'tab_settings_controls_keybinding': (591, 315),
    'tab_settings_controls_shiftclick': (642, 315),
    'tab_emotes_shrug': (656, 281),
    'tab_emotes_laugh': (613, 329),
    'tab_emotes_jig': (613, 378),
    'tab_magic_hometeleport': (570, 232),
    'tab_magic_windstrike': (596, 230),
    'mapCenter': (641, 84), 
    'mapTlc': (559, 5),
    'mapBrc': (717, 160),
    }

# Dict storing HUD locations and constants; setup finished in setHud call
hud = { 'init': False, 'mapRadius': 70, 'invSlotLen': 21 }
hud['mapImageCenter'] = (83, 79) #coords of map center used in makeMapList

# Grand Exchange interface coords (rel to origin)
geCoords = {
    'buy_0': (55, 153),
    'sell_0': (114, 146),
    'buy_1': (178, 148),
    'sell_1': (231, 154),
    'buy_2': (287, 147),
    'sell_2': (340, 155),
    'barTlc_0': (32, 158),
    'barBrc_0': (137, 171),
    'barTlc_1': (149, 158),
    'barBrc_1': (254, 171),
    'barTlc_2': (266, 158),
    'barBrc_2': (371, 171),
    'collect': (448, 68),
    'offer_portrait': (112, 110),
    'offer_coins': (406, 290),
    'quantity_minus': (53, 186),
    'quantity_plus': (246, 185),
    'quantity_all': (188, 211),
    'quantity_input': (232, 211),
    'price_minus': (274, 185),
    'price_plus': (467, 186),
    'price_percentminus': (289, 212),
    'price_percentplus': (450, 209),
    'price_input': (390, 213),
    'confirm': (252, 284),
    'back': (50, 288),
    'searchtext_tlc': (43, 377),
    'searchtext_brc': (167, 390),
    'search_firstresult': (28, 382),
    }

# Dict storing GE locations and constants; setup finished in setGE call
ge = { 'init': False, 'slotDim': (115, 110), 'labelDim': (113, 23) }
        
# Dict storing inventory; setup finished in setInv call
inv = {}

# Generate list of possible inventory items (items which can be detected)
possibleInvItems = []
for filename in glob.glob('images\\invitem*.png'):
    filename = filename[14:]
    filename = filename[:-4]
    if filename[-2:] == '_n':
        numbered = True
        filename = filename[:-2]
    else:
        numbered = False
    possibleInvItems.append({'name': filename, 'numbered': numbered})

# Game view coords (relative to origin)
coordConsts = {
    'viewTlc': (4, 4),
    'viewBrc': (516, 338),
    'wholeBrc': (765, 503),
    'viewCenter': (256, 167),
    }

# Vars for dividing game view into blocks to search
viewBlockLen = 37
viewPositions = None #Set after concentricList function definition 


"""
Functions
"""
##---------------------------------------------------------------------------
## Keyboard/mouse control
##---------------------------------------------------------------------------

# For the mouse movement function mouseTo, see file mouseMoveFunction.py.
# The definition is sufficiently complicated that it has its own file
# containing all of its helper functions.

# Click button using image search
def clickButton(imagename):
    bx, by = pag.locateCenterOnScreen(imagename)
    mouseTo(bx, by)
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# Click location given in pixel coordinates
def clickPix(pos):
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# Type a string
def typeString(string):
    startPAUSE = pag.PAUSE
    pag.PAUSE = 0
    for c in string:
        pag.press(c)
        time.sleep( random.uniform(0.05, 0.15) )
    pag.PAUSE = startPAUSE


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


##---------------------------------------------------------------------------
## Client window/coordinates management
##---------------------------------------------------------------------------

# Focus client window and bring to front - also set Ox, Oy
def focusClient(clientname):
    global Ox
    global Oy
    try:
        pag.keyDown('alt')
        SetForegroundWindow(find_window(title=clientname))
        pag.keyUp('alt')
    except:
        pag.keyUp('alt')
        return False
    if not Ox:
        try:
            Ox, Oy, trash1, trash2 = pag.locateOnScreen(images['origin'])
        except:
            logging.info('Could not find origin in helpers.focusClient')
    return True


# Start client and bring window to front
def startClient(clientname, clientpath):
    if focusClient(clientname):
        return True
    logging.info('Starting client: ' + clientname + ' at ' + clientpath)
    client = Application().start(clientpath)
    while not pag.locateCenterOnScreen(images['exbutton']):
        time.sleep(0.5)
    return focusClient(clientname)


# Set origin coords Ox, Oy if not already
def setOrigin():
    global Ox, Oy
    if not Ox:
        try:
            Ox, Oy, trash1, trash2 = pag.locateOnScreen(images['origin'])
        except:
            logging.warning('Could not find origin in helpers.setOrigin')


# Force reset of origin coords
# Note: this will throw an exception if origin is not found
def resetOrigin():
    global Ox, Oy
    Ox, Oy, trash1, trash2 = pag.locateOnScreen(images['origin'])


# Transform between pixel coord system and client window
# relative coord system
def coordsPixToClient(pixCoords):
    return (pixCoords[0] - Ox, pixCoords[1] - Oy)
def coordsClientToPix(clientCoords):
    return (Ox + clientCoords[0], Oy + clientCoords[1])


# Click a location given in relative coordinates
def clickClient(pos):
    pos = coordsClientToPix(pos)
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


##---------------------------------------------------------------------------
## User credentials/logging in and out
##---------------------------------------------------------------------------

# Check if logged in
def isLoggedIn():
    return pag.locateOnScreen(images['origin'])


# Log in
## Return True if logged in after function ends, False otherwise
## If character is completely new (starting in Tut Island), set tutorial=True
def login(username, password, world, tutorial=False):
    global Ox
    global Oy
    startPAUSE = pag.PAUSE
    
    if isLoggedIn():
        resetOrigin()
        return True
    logging.info('Logging in...')
    
    # Wait for login buttons to appear (max wait 20 sec)
    waitCounter = 0
    while not pag.locateCenterOnScreen(images['exbutton']):
        waitCounter += 1
        if waitCounter > 40:
            logging.warning('Login failed: could not find exbutton')
            return False
        time.sleep( random.uniform(0.5, 0.6) )

    # Select world
    pag.PAUSE = 0
    clickButton(images['switchbutton'])
    time.sleep( random.uniform(0.85, 1) )
    clickButton(images[str(world)])
    time.sleep( random.uniform(0.25, 0.4) )

    # Enter login data
    clickButton(images['exbutton'])
    time.sleep( random.uniform(0.25, 0.4) )
    pag.PAUSE = 0
    clickButton(images['loginfield'])
    for i in range(random.randint(40,50)):
        pag.press('backspace')
        time.sleep(random.uniform(0.05, 0.15))
    typeString(username)
    pag.press('tab')
    typeString(password)
    pag.PAUSE = 0.25

    # Click login button and wait
    clickButton(images['loginbutton'])
    logging.info('Logging in...')
    if not tutorial:
        confirmLoginKey = 'playbutton'
    else:
        confirmLoginKey = 'origin'
    start = time.time()
    while not pag.locateCenterOnScreen(images[confirmLoginKey]):
        time.sleep(0.5)
        # Wait max 15 sec to log in
        if time.time() - start > 15:
            logging.info('Login timed out after 15 seconds')
            ###
            ### Can check here to see why login failed and try again
            ###
            return False

    # Finish login and initialize Ox, Oy (if not already)
    if not tutorial:
        clickButton(images['playbutton'])
        while not pag.locateOnScreen(images['origin']):
            time.sleep(0.5)
    if not Ox:
        Ox, Oy, trash1, trash2 = pag.locateOnScreen(images['origin'])
    logging.info('Logged in')
    pag.PAUSE = startPAUSE
    return True


# Log out
def logout():
    clickButton(images['logoutTab'])
    time.sleep( random.uniform(0.3, 1.3) )
    clickButton(images['logoutbutton'])
    logging.info('Logged out')



##---------------------------------------------------------------------------
## Pixel/game view searching and general image processing
##---------------------------------------------------------------------------

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


# Convert an image of the map into a map list. Used in locateInMap
def makeMapList(im, whole):
    pix = im.load()
    xR = im.size[0]
    yR = im.size[1]
    r = hud['mapRadius']
    
    # Initialize mapList with all -1s
    mapList = [ [-1 for y in range(yR)] for y in range(xR) ]

    # If whole map, mark pixels outside of border with 0
    if whole:
        cen = hud['mapImageCenter']
        for x in range(xR):
            for y in range(yR):
                dx = cen[0] - x
                dy = cen[1] - y
                if dx*dx + dy*dy > r*r:
                    mapList[x][y] = 0

    # Mark other pixels as:
    # Red: 1, White: 2, Black: 3, Other: 4
    for x in range(xR):
        for y in range(yR):
            if mapList[x][y] == 0:
                continue
            p = pix[x,y][:3]
            r,g,b = p
            if r > 200 and g < 30 and b < 30: #red
                mapList[x][y] = 1
            elif r > 190 and g > 190 and b > 190: #white
                mapList[x][y] = 2
            elif r < 30 and g < 30 and b < 30: #black
                mapList[x][y] = 3
            else: #other
                mapList[x][y] = 4

    return mapList

    
# Mimic pyautogui.locate, but using image processing customized for map search
# Used in clickMapImage, searchMapImage
def locateInMap(needleImage, returnCenter=True):
    haystackImage = ImageGrab.grab(
            ( hud['mapTlc'][0], hud['mapTlc'][1],
              hud['mapBrc'][0], hud['mapBrc'][1] )
        )
    if isinstance(needleImage, str):
        needleImage = Image.open(needleImage)
    if ( needleImage.size[0] > haystackImage.size[0] or
         needleImage.size[1] > haystackImage.size[1] ):
        return None
    
    # Convert images to map lists
    needleList = makeMapList(needleImage, False)
    haystackList = makeMapList(haystackImage, True)

    # Search for needleList in haystackList
    for xH in range(haystackImage.size[0] - needleImage.size[0]):
        for yH in range(haystackImage.size[1] - needleImage.size[1]):
            # tlc of haystack is (xH, yH)
            mismatch = False
            for i in range(needleImage.size[0]):
                for j in range(needleImage.size[1]):
                    if haystackList[xH+i][yH+j] != needleList[i][j]:
                        mismatch = True
                        break
                if mismatch:
                    break
            if not mismatch: # if reach this line without a mismatch, found loc
                if returnCenter:
                    return ( xH + needleImage.size[0]//2,
                             yH + needleImage.size[1]//2 )
                else:
                    return (xH, yH)
    return None # if reached this line, checked entire image with no match


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
viewPositions = concentricList(14,9)


# Search for entity within bbox, returning list of possible locations.
# Search by dividing bbox into blocks and using blockProcess to determine
# if block is likely to contain entity.
def entitySearch(bbox, blockProcess, blockDimensions=(20,30)):
    # Get image
    im = ImageGrab.grab(bbox)
    pix = im.load()

    # Dividing bbox into blocks
    blockX, blockY = blockDimensions
    nblocksX = im.size[0]//blockX
    nblocksY = im.size[1]//blockY

    # Search for blocks meeting criterion given by blockProcess
    positions = []
    for i in range(nblocksX):
        for j in range(nblocksY):
            tlcX = blockX*i
            tlcY = blockY*j
            hueCount = 0
            if blockProcess(
                    xBounds=(tlcX, tlcX + blockX),
                    yBounds=(tlcY, tlcY + blockY),
                    pix=pix ):
                positions.append(
                    (bbox[0] + tlcX + blockX//2, bbox[1] + tlcY + blockY//2)
                    )
    return positions


# Attempt to open a dialog box at a position, then click a dialog option
# Return True if option found and clicked, False otherwise
## Note: may need to add ability to verify that you clicked the object you
## intended to, e.g. if you want to click something generic like 'examine'.
def dialogSelect(pos, option):
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.05, 0.1) )
    pag.click(button='right')
    time.sleep(0.05)
    optionPos = pag.locateCenterOnScreen('images\\dialog_' + option + '.png')
    if optionPos:
        mouseTo(optionPos[0], optionPos[1])
        time.sleep( random.uniform(0.05, 0.1) )
        pag.click()
        return True
    else:
        cPos = pag.position()
        mouseTo(cPos[0]+random.randint(-10,10),cPos[1]+random.randint(-30,-20))
        return False


# Attempt to click an option on an NPC's dialog box
# Return True if option found and clicked, False otherwise
## Note: may need to add ability to verify that you clicked the right NPC
def clickNPCdialog(bbox, blockProcess, option, name, timeLimit=90):
    start = time.time()
    while time.time() - start < timeLimit:
        positions = entitySearch(bbox, blockProcess)
        if len(positions) == 0:
            positions.append( coordsClientToPix((coordConsts['viewCenter'])) )
        for pos in positions:
            if dialogSelect(pos, option):
                return True
    logging.info('Failed to locate NPC: ' + name)
    return False


# Attempt to click an option on an entity's dialog box
# Return True if option found and clicked, False otherwise
## Note: may need to add ability to verify that you clicked the right entity
def clickEntityDialog(bbox, blockProcess, option, blockDimensions, name,
                      timeLimit=90):
    start = time.time()
    while time.time() - start < timeLimit:
        positions = entitySearch(bbox, blockProcess, blockDimensions)
        if len(positions) == 0:
            positions.append( coordsClientToPix((coordConsts['viewCenter'])) )
        for pos in positions:
            if dialogSelect(pos, option):
                return True
    logging.info('Failed to locate entity: ' + name)
    return False



##---------------------------------------------------------------------------
## HUD initialization/interaction/management (including inventory stuff)
##---------------------------------------------------------------------------

# Locate and store HUD locs
def setHud():
    global hud, hudCoords
    setOrigin()
    if hud['init']:
        return
    
    logging.info('Storing HUD locations...')
    ## Note: 'invSlots' stores the 'center' pixel of the inventory slot
    ## 'invSlotsTlcs' stores the TLC of a centered square over the slot
    # Add inventory slots
    hud['invSlots'] = []
    hud['invSlotsTlcs'] = []
    for j in range(7):
        for i in range(4):
            x = 578 + i*42
            y = 228 + j*36
            hud['invSlots'].append(coordsClientToPix((x,y)))
            hud['invSlotsTlcs'].append(coordsClientToPix((x-10,y-10)))

    # Add converted coords from hudCoords
    for key in hudCoords:
        hud[key] = coordsClientToPix(hudCoords[key])
        
    logging.info('HUD locations stored')


# Force reset of HUD locs
def resetHud():
    global hud
    hud['init'] = False
    setHud()


# Process inv number image (used by getInvNumber)
def processInvNumber(im):
    pix = im.load()
    
    # Locate columns with parts of digits (also adjust pix vals to ID later)
    cols = [False for x in range(im.size[0])]
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x,y] == (255, 255, 0):
                cols[x] = True
            else:
                pix[x,y] = (0,0,0)
    
    # Get column (x) ranges for each digit
    digitRanges = []
    onDigit = False
    lower = -1
    upper = -1
    for x in range(im.size[0]):
        if cols[x] and not onDigit:
            onDigit = True
            lower = x
        if not cols[x] and onDigit:
            onDigit = False
            upper = x
            digitRanges.append((lower, upper))

    # Identify number and return
    num = ''
    for r in digitRanges:
        digitIm = im.crop((r[0], 0, r[1], im.size[1]))
        digitIdentified = False
        for i in range(10):
            if pag.locate('images\\invnum'+str(i)+'.png', digitIm):
                num = num + str(i)
                digitIdentified = True
                break
        if not digitIdentified:
            logging.warning('Failed to identify digit in processInvNumber')
            digitIm.show()
    return int(num)


# Return number on a numbered item in given slot
def getInvNumber(slot):
    center = hud['invSlots'][slot]
    tlc = (center[0] - 17, center[1] - 15)
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+40, tlc[1]+8))
    return processInvNumber(im)


# Helper for inv item detection: Find pixels of inv item shot that are equal
# to the empty inv shot and recolor them white
def processInvItemShot(pix, slot, numbered=False):
    emptyIm = Image.open('images\\emptyinv' + str(slot) + '.png')
    emptyPix = emptyIm.load()
    for x in range(emptyIm.size[0]):
        for y in range(emptyIm.size[1]):
            if pix[x,y] == emptyPix[x,y]:
                pix[x,y] = (255,255,255)
    if numbered: # remove top four pixel rows containing numbers
        for x in range(emptyIm.size[0]):
            for y in range(5):
                pix[x,y] = (255,255,255)


# Check if inventory slot is empty
def isInvSlotEmpty(slot):
    tlc = hud['invSlotsTlcs'][slot]
    size = hud['invSlotLen']
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    return pag.locate('images\\emptyinv' + str(slot) + '.png', im)


# Check for coins in slot; return coins data object if so, False if not
def isCoinsInSlot(slot):
    tlc = hud['invSlotsTlcs'][slot]
    size = hud['invSlotLen']
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    pix = im.load()
    processInvItemShot(pix, slot, numbered=True)
    for n in range(10):
        if pag.locate(im, 'images\\invcoins'+str(n)+'.png'):
            return { 'slot': slot, 'amount': getInvNumber(slot) }
    return False


# Return coins data object storing inv slot and amount of coins (or None)
def getInvCoins():
    for i in range(28):
        coins = isCoinsInSlot(i)
        if coins:
            return coins
    return None


# Check if particular item is in inventory slot
def isItemInSlot(name, slot, numbered=False):
    if name=='Coins':
        return isCoinsInSlot(slot)
    tlc = hud['invSlotsTlcs'][slot]
    size = hud['invSlotLen']
    im = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    pix = im.load()
    processInvItemShot(pix, slot, numbered=numbered)
    for item in possibleInvItems:
        if item['name'] == name:
            if numbered:
                itemIm = Image.open('images\\invitem' + name + '_n.png')
            else:
                itemIm  = Image.open('images\\invitem' + name + '.png')
            return pag.locate(itemIm, im)
    logging.warning('Image for item ' + name + ' not found.')
    return False


# Return name of item in inventory slot (or 'empty' or 'unkown')
# If data==True, return full item data:
#   {name: str, numbered: bool, quantity: int} 
def getItemInSlot(slot, data=False):
    if isInvSlotEmpty(slot):
        if data:
            return { 'name': 'empty', 'numbered': False, 'quantity': 0 }
        return 'empty'
    tlc = hud['invSlotsTlcs'][slot]
    size = hud['invSlotLen']
    imNumbered = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    imNormal = ImageGrab.grab((tlc[0], tlc[1], tlc[0]+size, tlc[1]+size))
    pixNumbered = imNumbered.load()
    pixNormal = imNormal.load()
    processInvItemShot(pixNumbered, slot, numbered=True)
    processInvItemShot(pixNormal, slot, numbered=False)
    # Check for regular items
    for item in possibleInvItems:
        if item['numbered']:
            itemIm = Image.open('images\\invitem'+item['name']+'_n.png')
            if pag.locate(itemIm, imNumbered):
                if data:
                    return {
                        'name': item['name'],
                        'numbered': True,
                        'quantity': getInvNumber(slot)
                        }
                return item['name']
        else: #not numbered
            itemIm  = Image.open('images\\invitem'+item['name']+'.png')
            if pag.locate(itemIm, imNormal):
                if data:
                    return {
                        'name': item['name'],
                        'numbered': False,
                        'quantity': 1
                        }
                return item['name']
    # If not identified among regular items, check for coins in slot
    coins = isCoinsInSlot(slot)
    if coins:
        if data:
            return {
                'name': 'Coins',
                'numbered': True,
                'quantity': coins['amount']
                }
        return 'Coins'
    # Item not recognized, so return 'unknown'
    if data:
        return { 'name': 'unkown', 'numbered': False, 'quantity': 1 }
    return 'unknown'


# Return first inv slot containing item, or -1 if not found
def searchInv(name, numbered=False):
    for i in range(28):
        if isItemInSlot(name, i, numbered=numbered):
            return i
    return -1


# Get first empty inventory slot; return -1 if full
def firstEmptyInvSlot():
    for i in range(28):
        if isInvSlotEmpty(i):
            return i
    return -1


# Get last empty inventory slot from the end
# Explanation: start at end, and move backwards until you reach nonempty slot.
# If return 28, last inv slot is nonempty.
# If return -1, inventory is empty.
def endLastEmptyInvSlot():
    for i in range(27,-1,-1):
        if not isInvSlotEmpty(i):
            return (i+1)
    return -1


# Check for full inventory
def isInvFull():
    return (firstEmptyInvSlot() < 0)


# Empty inventory (drop ALL items)
## Note: must have shift+click dropping enabled
def dropAllInv():
    pag.keyDown('shift')
    for pos in hud['invSlots']:
        mouseTo(pos[0], pos[1])
        pag.click()
    pag.keyUp('shift')


# Drop all of a certain item
## Note: must have shift+click dropping enabled
def dropAllItem(name, numbered=False):
    pag.keyDown('shift')
    for i in range(28):
        if isItemInSlot(name=name, slot=i, numbered=numbered):
            pos = hud['invSlots'][i]
            mouseTo(pos[0], pos[1])
            time.sleep( random.uniform(0.05, 0.1) )
            pag.click()
    pag.keyUp('shift')


# Drop whatever is in a certain slot
## Note: must have shift+click dropping enabled
def dropSlot(slot):
    pag.keyDown('shift')
    pos = hud['invSlots'][slot]
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.05, 0.1) )
    pag.click()
    pag.keyUp('shift')


# Drop whatever is in a list of slots
## Note: must have shift+click dropping enabled
def dropSlots(slots):
    pag.keyDown('shift')
    for slot in slots:
        pos = hud['invSlots'][slot]
        mouseTo(pos[0], pos[1])
        time.sleep( random.uniform(0.05, 0.1) )
        pag.click()
        time.sleep( random.uniform(0.15, 0.25) )
    pag.keyUp('shift')


# Click inventory slot
def clickInvSlot(slot):
    pos = hud['invSlots'][slot]
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.05, 0.1) )
    pag.click()


# Click item somewhere in inventory; return slot clicked (or -1 if not found)
def clickInvItem(name, numbered=False):
    slot = searchInv(name, numbered=numbered)
    if slot < 0:
        return -1
    else:
        clickInvSlot(slot)
        return slot


# Click a right-click dialog box option on an item in inventory
def invDialog(option, name=None, slot=None, numbered=False):
    if not name and not slot:
        logging.info('No inv item info passed to invDialog')
        return False
    if name:
        slot = searchInv(name, numbered=numbered)
        if slot < 0:
            logging.info('In invDialog; failed to find inv item: ' + name)
            return False

    pos = hud['invSlots'][slot]
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.05, 0.1) )
    pag.click(button='right')
    time.sleep(0.05)
    optionPos = pag.locateCenterOnScreen('images\\dialog_' + option + '.png')
    if optionPos:
        mouseTo(optionPos[0], optionPos[1])
        time.sleep( random.uniform(0.05, 0.1) )
        pag.click()
        return True
    else:
        cPos = pag.position()
        mouseTo(cPos[0]+random.randint(-10,10),cPos[1]+random.randint(-30,-20))
        return False


# Use one inventory item with another; can provide either names of the items
# or inventory slots
def useWithInv(names=None, slots=None, numbered=(False, False)):
    if not names and not slots:
        logging.info('No inv item info passed to useWithInv')
        return False
    if names:
        slots = (
            searchInv(names[0], numbered=numbered[0]),
            searchInv(names[1], numbered=numbered[1])
            )
        if slots[0] < 0 or slots[1] < 0:
            logging.info('In useWithInv; failed to find inv items: '
                         + str(names))
            return False

    if not invDialog(option='use', slot=slots[0]):
        logging.info('Failed to click use on slot ' + str(slots[0]))
        return False
    time.sleep( random.uniform(0.05, 0.15) )
    clickInvSlot(slots[1])
    return True


# Store inventory information
def setInv():
    global inv
    for i in range(28):
        inv[i] = getItemInSlot(i, data=True)
    logging.info('Set inventory')


# Click a HUD element
def clickHud(element):
    pos = hud[element]
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# Click randomly in a neutral part of the HUD that won't do anything
def clickNeutral():
    x = math.floor(random.randint(518, 542))
    y = math.floor(random.randint(208, 464))
    x, y = coordsClientToPix((x,y))
    mouseTo(x,y)
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# Set run to 'on' or 'off'
def setRun(setting):
    if pag.locateCenterOnScreen('images\\map_run_' + setting + '.png'):
        return
    clickHud('run')


# Click map at given coords (relative to map center)
def clickMap(x, y):
    r = hud['mapRadius']
    if (x*x + y*y > r*r):
        logging.warning('Invalid position passed to clickMap')
        return
    center = hud['mapCenter']
    mouseTo(center[0]+x, center[1]+y, precise=True)
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# Click preset direction on map
def clickMapDirection(direction, multiplier=1):
    direction = direction.lower()
    r = hud['mapRadius'] * multiplier
    rdiag = ( math.floor(0.85 * r/math.sqrt(2)) ) * multiplier
    if direction == 'n':
        clickMap(0, -r)
    elif direction == 's':
        clickMap(0, r)
    elif direction == 'e':
        clickMap(r, 0)
    elif direction == 'w':
        clickMap(-r, 0)
    elif direction == 'ne':
        clickMap(rdiag, -rdiag)
    elif direction == 'nw':
        clickMap(-rdiag, -rdiag)
    elif direction == 'sw':
        clickMap(-rdiag, rdiag)
    elif direction == 'se':
        clickMap(rdiag, rdiag)
    else:
        logging.info('Invalid click map direction: ' + direction)


# Walk a series of map directions
def walkSeries(directions):
    for d in directions:
        clickMapDirection(d)
        time.sleep( random.uniform(8.5, 8.6) )

# Run a series of map directions
def runSeries(directions):
    for d in directions:
        clickMapDirection(d)
        time.sleep( random.uniform(5.5, 5.6) )


# Search map for a reference image until time expires. Return pixel coords
# if found, None if not
def searchMapImage(refImage, timeLimit=60, center=True):
    start = time.time()
    while time.time() - start < timeLimit:
        pos = locateInMap(refImage, center)
        if pos:
            return pos
        else:
            time.sleep(1)
    return None


# Try to click a reference image in map until time expires
def clickMapImage(refImage, timeLimit=60, center=True):
    pos = searchMapImage(refImage, timeLimit=timeLimit, center=center)
    if pos:
        mouseTo(hud['mapTlc'][0]+pos[0], hud['mapTlc'][1]+pos[1], precise=True)
        time.sleep( random.uniform(0.15, 0.3) )
        pag.click()
        return True
    else:
        return False


# Reset camera to north-facing top-down view
def resetCamera():
    clickHud('compass')
    holdKey('up', 2)


# Rotate camera slightly
def perturbCamera():
    if random.randint(0, 3) == 0:
        holdKey('left', random.uniform(0.15, 0.35))
    else:
        holdKey('right', random.uniform(0.15, 0.35))



##---------------------------------------------------------------------------
## Grand Exchange / Bank 
##---------------------------------------------------------------------------


# Set GE coords
def setGE():
    global ge, geCoords
    setOrigin()
    if ge['init']:
        return
    
    logging.info('Storing GE locations...')
    # Adding more geCoords
    # Coords for offer slots:
    slotsTlc = (27, 83)
    slotsBrc = (142, 193)
    slotXlen = ge['slotDim'][0]
    slotYlen = ge['slotDim'][1]
    slotXd = 2
    slotYd = 10
    for i in range(4):
        for j in range(2):
            tlc = (slotsTlc[0] + (slotXlen+slotXd)*i,
                   slotsTlc[1] + (slotYlen+slotYd)*j)
            geCoords['slot' + str(4*j+i) + '_tlc'] = tlc
            geCoords['slot' + str(4*j+i) + '_brc'] = (tlc[0]+slotXlen,
                                                      tlc[1]+slotYlen)
            geCoords['slot' + str(4*j+i) + '_labelBrc'] = (tlc[0]+113,
                                                           tlc[1]+23)
    # Coords for search result texts:
    searchTextTlc = (49, 370)
    searchTextBrc = (171, 398)
    xDisp = 161
    yDisp = 32
    for i in range(3):
        for j in range(3):
            tlc = (searchTextTlc[0] + xDisp*i, searchTextTlc[1] + yDisp*j)
            brc = (searchTextBrc[0] + xDisp*i, searchTextBrc[1] + yDisp*j)
            geCoords['searchText' + str(3*j+i) + '_tlc'] = tlc
            geCoords['searchText' + str(3*j+i) + '_brc'] = brc

    # Add converted coords from geCoords
    for key in geCoords:
        ge[key] = coordsClientToPix(geCoords[key])
        
    logging.info('GE locations stored')


# Force reset of GE coords
def resetGE():
    global ge
    ge['init'] = False
    setGE()


# Click a GE element
def clickGE(element):
    pos = ge[element]
    mouseTo(pos[0], pos[1])
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()


# blockProcess function to search for npc GE Clerk
def processClerk(xBounds, yBounds, pix):
    blue = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = getHueFromRgb(pix[x,y])
            if hue < 177 and hue > 172:
                blue += 1
        if blue > 40:
            return True
    return False


# Open GE interface by right-click dialog on npc Grand Exchange Clerk.
# Return True once interface is open or False if cannot click clerk or timeout.
def openGEInterface(timeLimit=15):
    if pag.locateOnScreen('images\\ge_ge.png'):
        return True
    tlcEntire = coordsClientToPix( coordConsts['viewTlc'] )
    brcEntire = coordsClientToPix( coordConsts['viewBrc'] )
    if not clickNPCdialog(
            bbox=(tlcEntire[0], tlcEntire[1], brcEntire[0], brcEntire[1]),
            blockProcess=processClerk,
            option='exchange',
            name='GE Clerk'
            ):
        logging.info('Failed to locate GE Clerk')
        return False
    start = time.time()
    while time.time() - start < timeLimit:
        if pag.locateOnScreen('images\\ge_ge.png'):
            return True
        time.sleep(1)
    if pag.locateOnScreen('images\\ge_ge.png'):
        return True
    logging.info('GE Interface open timeout after ' + str(timeLimit)
                 + ' seconds')
    return False 


# Process GE label text for comparison in getGESlotLabel
def processGELabelText(im):
    pix = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            p = pix[x,y]
            if p[0] != 255 or p[1] != 152 or p[2] != 31:
                pix[x,y] = (0,0,0)


# Return label (empty, buy, or sell) of GE slot
def getGESlotLabel(slot):
    slotTlc = ge['slot' + str(slot) + '_tlc']
    slotDim = ge['slotDim']
    labelDim = ge['labelDim']
    imSlot = ImageGrab.grab((slotTlc[0], slotTlc[1],
                             slotTlc[0]+labelDim[0], slotTlc[1]+labelDim[1]))
    processGELabelText(imSlot)
    if pag.locate('images\\ge_empty.png', imSlot):
        return 'empty'
    if pag.locate('images\\ge_buy.png', imSlot):
        return 'buy'
    if pag.locate('images\\ge_sell.png', imSlot):
        return 'sell'
    logging.warning('In getGESlotLabel: failed to identify label')
    return False


# Return first offer slot of given kind (e.g. 'empty') or -1 if none
def getFirstOfferSlot(kind, f2p=True):
    if f2p:
        rangeLimit = 3
    else:
        rangeLimit = 8
    for i in range(rangeLimit):
        if getGESlotLabel(i) == kind:
            return i
    return -1


# Make char schematics out of each char in the string of a search text image.
# Also return locations of spaces
## Used in readGESearchSlot
def makeCharSchematics(im):
    pix = im.load()
    
    # Locate columns with parts of chars (also adjust pix vals to ID later)
    cols = [False for x in range(im.size[0])]
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x,y] == (0,0,0):
                cols[x] = True
            else:
                pix[x,y] = (255,255,255)

    # Get column (x) ranges for each char
    charColRanges = []
    onChar = False
    lower = -1
    upper = -1
    for x in range(im.size[0]):
        if cols[x] and not onChar:
            onChar = True
            lower = x
        if not cols[x] and onChar:
            onChar = False
            upper = x
            charColRanges.append((lower, upper)) #note: one-past upper bound

    # Identify spaces
    spaces = []
    for i in range(len(charColRanges) - 1):
        spaceLen = charColRanges[i+1][0] - charColRanges[i][1]
        if spaceLen > 3:
            spaces.append(i)

    # Get row (y) ranges for each char
    charRowRanges = []
    for i in range(len(charColRanges)):
        cr = charColRanges[i]
        minR = im.size[1]
        maxR = -1
        for x in range(cr[0], cr[1]):
            for y in range(im.size[1]):
                if pix[x,y] == (0,0,0):
                    if y < minR:
                        minR = y
                    if y > maxR:
                        maxR = y
        charRowRanges.append((minR, maxR+1)) #note: one-past upper bound

    # Construct the char schematic objects
    schematics = []
    for i in range(len(charRowRanges)):
        cr = charColRanges[i]
        rr = charRowRanges[i]
        charIm = im.crop((cr[0], rr[0], cr[1], rr[1]))
        charPix = charIm.load()
        schematic = [[False for y in range(rr[0], rr[1])] for x in range(cr[0], cr[1])]
        for x in range(cr[1]-cr[0]):
            for y in range(rr[1]-rr[0]):
                if charPix[x,y] == (0,0,0):
                    schematic[x][y] = True
        schematics.append(schematic)

    return (schematics, spaces)


# Read GE search result slot text
def readGESearchSlot(slot):
    tlc = ge['searchText' + str(slot) + '_tlc']
    brc = ge['searchText' + str(slot) + '_brc']
    im = ImageGrab.grab((tlc[0], tlc[1], brc[0], brc[1]))
    
    charPatterns, spaces = makeCharSchematics(im)
    string = ''
    spaceCounter = 0
    
    for i in range(len(charPatterns)):
        pattern = charPatterns[i]
        for pat in gescp.patterns:
            if len(pattern) != len(pat['schematic']):
                continue
            if len(pattern[0]) != len(pat['schematic'][0]):
                continue
            mismatch = False
            for x in range(len(pattern)):
                for y in range(len(pattern[0])):
                    if pattern[x][y] != pat['schematic'][x][y]:
                        mismatch = True
                        break
                if mismatch:
                    break
            if mismatch:
                continue
            string = string + pat['char']
            if spaceCounter < len(spaces) and spaces[spaceCounter] == i:
                string = string + ' '
                spaceCounter += 1
            break
            
    return string


# Click the GE search result with the given text
def clickGESearchResult(text):
    for i in range(9):
        if readGESearchSlot(i) == text:
            logging.info(text + ' located in search result slot ' + str(i))
            tlc = ge['searchText' + str(i) + '_tlc']
            brc = ge['searchText' + str(i) + '_brc']
            pos = ((tlc[0] + brc[0])//2, (tlc[1] + brc[1])//2)
            pos = (pos[0] + random.randint(-4,4), pos[1] + random.randint(-4,4))
            mouseTo(pos[0], pos[1])
            time.sleep( random.uniform(0.05, 0.15) )
            pag.click()
            return True
    logging.info(text + ' not found')
    return False


# Starting on GE screen, sell all of an item in inventory on the GE
# and collect the money to inventory. Expect to sell instantly.
def sellAndCollect(itemSlot):
    # Detect available offer slot (within first 3 f2p slots)
    offerSlot = getFirstOfferSlot('empty')
    if offerSlot < 0:
        logging.info('No available offer slots')
        return False

    # Click sell
    clickGE('sell_' + str(offerSlot))
    time.sleep( random.uniform(1, 1.1) )

    # Enter sell offer
    clickInvSlot(itemSlot)
    time.sleep( random.uniform(0.8, 0.9) )
    clickGE('quantity_all')
    time.sleep( random.uniform(0.2, 0.3) )
    for i in range(8):
        clickGE('price_percentminus')
        time.sleep( random.uniform(0.05, 0.1) )
    clickGE('confirm')
    time.sleep( random.uniform(4.1, 4.2) )
    clickGE('collect')
    return True


# Starting on GE screen, enter a buy offer for quantity of items at the
# given price and collect items (or notes) to inventory. Expect instant buy.
def buyAndCollect(item, quantity, price):
    # Click an empty slot's buy button
    offerSlot = getFirstOfferSlot('empty')
    if offerSlot < 0:
        logging.info('No available offer slots')
        return False
    clickGE('buy_' + str(offerSlot))
    time.sleep( random.uniform(2.5, 2.6) )
    
    # Enter item and click search result
    typeString(item)
    time.sleep( random.uniform(1.4, 1.5) )
    if not clickGESearchResult(item):
        return False
    time.sleep( random.uniform(1.2, 1.3) )

    # Enter quantity and price
    if quantity < 1:
        logging.info('Quantity < 1 in instantBuy')
        return False
    if quantity > 1:
        clickGE('quantity_input')
        time.sleep( random.uniform(1.5, 1.6) )
        typeString(str(quantity))
        time.sleep( random.uniform(0.1, 0.15) )
        pag.press('enter')
        time.sleep( random.uniform(1.2, 1.35) )
    clickGE('price_input')
    time.sleep( random.uniform(1.5, 1.6) )
    typeString(str(price))
    time.sleep( random.uniform(0.1, 0.15) )
    pag.press('enter')
    time.sleep( random.uniform(1.2, 1.35) )

    # Confirm and collect
    clickGE('confirm')
    time.sleep( random.uniform(4, 5.2) )
    clickGE('collect')
    return True


# blockProcess function for standard Bank booth
def processBankBooth(xBounds, yBounds, pix):
    blue = 0
    pink = 0
    red = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = getHueFromRgb(pix[x,y])
            if hue == 26:
                blue += 1
            elif hue == 25:
                pink += 1
            elif hue == 22:
                red += 1
        if blue > 30 and pink > 30 and red > 2:
            return True
    return False


# Open bank interface by right-clicking bank booths
# To open bank at a different style of booth, pass a different blockProcess
def openBankInterface(timeLimit=15, blockProcess=processBankBooth):
    if pag.locateOnScreen('images\\bank_bank.png'):
        return True
    tlcEntire = coordsClientToPix( coordConsts['viewTlc'] )
    brcEntire = coordsClientToPix( coordConsts['viewBrc'] )
    if not clickEntityDialog(
            bbox=(tlcEntire[0], tlcEntire[1], brcEntire[0], brcEntire[1]),
            blockProcess=blockProcess,
            option='bank',
            blockDimensions = (30, 30),
            name='Bank booth'
            ):
        logging.info('Failed to locate Bank booth')
        return False
    start = time.time()
    while time.time() - start < timeLimit:
        if pag.locateOnScreen('images\\bank_bank.png'):
            return True
        time.sleep(1)
    if pag.locateOnScreen('images\\bank_bank.png'):
        return True
    logging.info('Bank interface open timeout after ' + str(timeLimit)
                 + ' seconds')
    return False



##---------------------------------------------------------------------------
## Misc.
##---------------------------------------------------------------------------

# Check if under attack by looking for health bar
def isUnderAttack():
    global Ox, Oy
    im = ImageGrab.grab((Ox + 222, Oy + 129, Ox + 298, Oy + 181))
    if pag.locate('images\\hbargreen.png', im):
        return True
    if pag.locate('images\\hbarred.png', im):
        return True
    return False

# Run away until not under attack
def evade():
    r = hud['mapRadius']
    clickMap(0,-r)
    while isUnderAttack():
        logging.info('Under attack')
        if random.randint(0,1) == 0:
            clickMap(0,-r) # north
        else:
            clickMap(-r,0) # west
        time.sleep(3)

# Update the status of an account in private_accounts
def updateAccountStatus(email, password, newStatus):
    # Ensure new status value is allowed
    allowedStatusValues = [
        'banned',           # account banned
        'new',              # never logged in
        'tutorial',         # on tutorial island
        'done tutorial',    # completed tutorial island
        ]
    if not newStatus in allowedStatusValues:
        logging.info('Bad newStatus in updateAccountStatus: ' + newStatus)
        return False

    # Update value
    updated = False
    for i in range(len(accounts)):
        acc = accounts[i]
        creds = acc['credentials']
        if creds[0] == email and creds[1] == password:
            accounts[i]['status'] = newStatus
            updated = True
            break
    if not updated:
        logging.info('Could not find account in private_accounts: ' + email)
        return False

    # Save to private_accounts.py
    file = open('private_accounts.py', 'w')
    file.write('accounts = ' + pprint.pformat(accounts))
    file.close()
    return True


# Complete an NPC chat sequence
## Pass a list of chat events. Event format:
## { 'type': string,  'data': string }
## 'type' is either 'continue' or 'choice'. If 'choice', then 'data' is the
## number (in string form) of the choice you want to select.
def chat(events):
    for e in events:
        if e['type'] == 'continue':
            pag.press('space')
        elif e['type'] == 'choice':
            pag.press(e['data'])
        else:
            logging.warning('Invalid chat event type: ' + e['type'])
            return
        logging.info('Processed chat event: ' + e['type'])
        time.sleep( random.uniform(2, 2.5) )


