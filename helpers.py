#! python3

"""
helpers.py

Contains general functions and variables used by
multiple different scripts.
"""

import time, sys, logging, random, math
from mouseMoveFunction import mouseTo
import pywinauto
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
from pywinauto.application import Application
import pyautogui as pag

pag.PAUSE = 0.25


"""----------------------------------------------------------------------------
Variables
"""
# Bank of images
images = {
    'exbutton': 'images\\existinguserbutton.png',
    'switchbutton': 'images\\clicktoswitchbutton.png',
    '393': 'images\\world393button.png',
    'loginbutton': 'images\\loginbutton.png',
    'playbutton': 'images\\clickheretoplaybutton.png',
    'origin': 'images\\origin.png',
    'equipmentTab': 'images\\equipment.png',
    'inventoryTab': 'images\\inventory.png',
    'logoutTab': 'images\\logouttab.png',
    'logoutbutton': 'images\\logoutbutton.png',
}

# Origin of coord system relative to client window
# These are intialized in the startClient call
Ox = None
Oy = None

# Dict storing HUD locations; initialized in getHud call
hud = None

# User password, initialized after user enters it in login GUI
pw = None

# Useful coords (relative to origin)
coordConsts = {
    'viewTlc': (4, 4),
    'viewBrc': (516, 338),
    'wholeBrc': (765, 503),
    }

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


"""----------------------------------------------------------------------------
Functions
"""
# Helper function for mouseTo: computes displacement along v2
def fDisp1(t):
    return math.sin(t*t*6.283)
def fDisp2(t):
    return 6.75*(t*t - t*t*t)


# Click button using image search
def clickButton(imagename):
    bx, by = pag.locateCenterOnScreen(imagename)
    #pag.moveTo(bx, by)
    mouseTo(bx, by)
    time.sleep(0.1)
    pag.click()


# Focus client window and bring to front
def focusClient(clientname):
    global Ox
    global Oy
    try:
        pag.keyDown('alt')
        SetForegroundWindow(find_window(title=clientname))
        pag.keyUp('alt')
    except:
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
    logging.info('Starting client...')
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


# Check if logged in
def isLoggedIn():
    return pag.locateOnScreen(images['origin'])


# Log in
def login(username, world):
    global Ox
    global Oy
    global pw
    startPAUSE = pag.PAUSE
    
    if isLoggedIn():
        resetOrigin()
        return
    
    # Wait for login buttons to appear (max wait 20 sec)
    waitCounter = 0
    while not pag.locateCenterOnScreen(images['exbutton']):
        waitCounter += 1
        if waitCounter > 40:
            logging.warning('Login failed: could not find exbutton')
            return
        time.sleep(0.5)

    # Select world
    pag.PAUSE = 0.25
    clickButton(images['switchbutton'])
    clickButton(images[str(world)])

    # Enter login data
    clickButton(images['exbutton'])
    # Get password if not already initialized
    if not pw:
        promptText = ('Username: ' + username +
            '\n(To change username, edit file loginInfo.py)' +
            '\nEnter password:')
        password = pag.password(text=promptText, title='Login')
        if not password:
            logging.info('User cancelled login.')
            return
        if len(password) == 0:
            logging.info('User submitted empty password.')
            return
        pw = password
    pag.PAUSE = 0
    for i in range(len(pw)):
        pag.press(pw[i])
        time.sleep(0.05 + random.random()*0.15)
    pag.press('tab')
    for i in range(50):
        pag.press('backspace')
        time.sleep(0.05 + random.random()*0.15)
    for i in range(len(username)):
        pag.press(username[i])
        time.sleep(0.05 + random.random()*0.15)
    pag.PAUSE = 0.25

    # Log in (initialize Ox, Oy if not already)
    clickButton(images['loginbutton'])
    logging.info('Logging in...')
    while not pag.locateCenterOnScreen(images['playbutton']):
        time.sleep(0.5)
    clickButton(images['playbutton'])
    while not pag.locateOnScreen(images['origin']):
        time.sleep(0.5)
    if not Ox:
        Ox, Oy, trash1, trash2 = pag.locateOnScreen(images['origin'])
    logging.info('Logged in')
    
    pag.PAUSE = startPAUSE


# Log out
def logout():
    clickButton(images['logoutTab'])
    time.sleep(0.5)
    clickButton(images['logoutbutton'])
    logging.info('Logged out')


# Locate and store HUD locs
def setHud():
    global hud
    setOrigin()
    if hud:
        return
    time.sleep(0.5)
    logging.info('Storing HUD locations...')
    hud = {}
    hud['compass'] = coordsClientToPix((561, 20))
    hud['inventoryTab'] = pag.locateOnScreen(images['inventoryTab'])
    ## Note: 'invSlots' stores the 'center' pixel of the inventory slot
    ## 'invSlotsTlcs' stores the TLC of a centered 9x9 square over the slot
    hud['invSlots'] = []
    hud['invSlotsTlcs'] = []
    for j in range(7):
        for i in range(4):
            x = 578 + i*42
            y = 228 + j*36
            hud['invSlots'].append(coordsClientToPix((x,y)))
            hud['invSlotsTlcs'].append(coordsClientToPix((x-4,y-4)))
    hud['invSlotLen'] = 9
    hud['equipmentTab'] = pag.locateOnScreen(images['equipmentTab'])
    hud['equipSlots'] = {
        'weapon': coordsClientToPix((586, 305))
    }
    hud['mapCenter'] = coordsClientToPix((641, 84))
    hud['mapRadius'] = 70
    logging.info('HUD locations stored')

# Force reset of HUD locs
def resetHud():
    hud = None
    setHud()
    

        


