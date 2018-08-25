#! python3

"""
Script for completing tutorial island
"""

import time
import logging
import random
import pyautogui as pag
from PIL import ImageGrab
from PIL import Image
import helpers
from mouseMoveFunction import mouseTo
import woodcutter

logging.getLogger().setLevel(logging.INFO)


"""
Functions
"""

def designCharacter():
    """Design random character, complete character design screen"""

    if not pag.locateCenterOnScreen('images\\tut_acceptbutton.png'):
        logging.info('Character design is already done')
        return

    # Create random design choices object
    designChoices = {
        'gender': random.randint(0,1),
        'clothes': [],
        'colors': [],
        }
    for i in range(7):
        designChoices['clothes'].append( random.randint(-7,7) )
    for i in range(5):
        designChoices['colors'].append( random.randint(-7,7) )

    # Set gender
    if designChoices['gender'] == 0:
        helpers.clickButton('images\\tut_femalebutton.png')

    # Set clothes options
    tlx, tly = helpers.coordsClientToPix((50, 90))
    dx = 115
    dy = 35
    for i in range(len(designChoices['clothes'])):
        clicks = designChoices['clothes'][i]
        if clicks < 0:
            mouseTo(tlx, tly + i*dy)
            clicks = -1*clicks
        elif clicks > 0:
            mouseTo(tlx + dx, tly + i*dy)
        else:
            continue
        for j in range(clicks):
            if random.randint(0,8) == 0:
                pos = pag.position()
                mouseTo(
                    pos[0] + random.randint(-4,4),
                    pos[1] + random.randint(-4,4)
                    )
                pag.click()
            time.sleep(random.uniform(0.1, 1))
        time.sleep(random.uniform(0.5, 1.5))

    # Set colors options
    tlx, tly = helpers.coordsClientToPix((350, 95))
    for i in range(len(designChoices['colors'])):
        clicks = designChoices['colors'][i]
        if clicks < 0:
            mouseTo(tlx, tly + i*dy)
            clicks = -1*clicks
        elif clicks > 0:
            mouseTo(tlx + dx, tly + i*dy)
        else:
            continue
        for j in range(clicks):
            if random.randint(0,8) == 0:
                pos = pag.position()
                mouseTo(
                    pos[0] + random.randint(-4,4),
                    pos[1] + random.randint(-4,4)
                    )
            pag.click()
            time.sleep(random.uniform(0.1, 1))
        time.sleep(random.uniform(0.5, 1.5))
            
    # Click accept to exit design screen
    helpers.clickButton('images\\tut_acceptbutton.png')


def processRunescapeGuide(xBounds, yBounds, pix):
    """blockProcess function to search for npc RuneScape Guide"""

    threshold = 20
    hueCount = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 2 or hue == 3:
                hueCount += 1
        if hueCount > threshold:
            return True
    if hueCount > threshold:
        return True
    return False

def processDoor(xBounds, yBounds, pix):
    """blockProcess function to search for entity Door"""

    hues = { 26: 0, 27: 0, 25: 0, }
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue in hues:
                hues[hue] += 1
        if hues[26] > 20 and (hues[27] > 0 or hues[25] > 0):
            return True
    return False

def processSurvivalExpert(xBounds, yBounds, pix):
    """blockProcess function to search for npc Survival Expert"""

    threshold = 20
    hueCount = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 2 or hue == 3:
                hueCount += 1
        if hueCount > threshold:
            return True
    if hueCount > threshold:
        return True
    return False

def processFishingSpot(xBounds, yBounds, pix):
    """blockProcess function to search for entity Fishing spot"""

    threshold = 1
    hueCount = 0
    hues = [136, 138, 139, 149, 206]
    rgbs = [(183, 176, 182), (174, 188, 222), (168, 195, 229),
            (148, 186, 230), (145, 176, 217), (133, 171, 226),
            (126, 173, 217), (117, 171, 226), (174, 204, 225),
            (114, 149, 179), (111, 151, 216), (109, 150, 209),
            (106, 155, 216), (99, 127, 168), (96, 156, 221), (94, 120, 159),
            (91, 147, 209), (89, 131, 173), (85, 117, 163), (94, 152, 216)]
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            if pix[x,y] in rgbs:
                hueCount += 1
        if hueCount > threshold:
            return True
    if hueCount > threshold:
        return True
    return False

def processFire(xBounds, yBounds, pix):
    """blockProcess function to search for entity Fire"""

    hueCounts = {26: 0, 27: 0, 29: 0}
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue in hueCounts:
                hueCounts[hue] += 1
        if hueCounts[29] > 30 and hueCounts[26] > 2 and hueCounts[27] > 2:
            return True
    return False

def processChef(xBounds, yBounds, pix):
    """blockProcess function to search for npc Master Chef"""

    white = 0
    brown = 0
    green = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 0:
                white += 1
            elif hue == 80 or hue == 81:
                green += 1
            elif hue == 18:
                brown += 1
        if white > 30 and green > 5 and brown > 5:
            return True
    if white > 30 and green > 5 and brown > 5:
        return True
    return False

def processRange(xBounds, yBounds, pix):
    """blockProcess function to search for entity Range"""

    counts = {'black': 0, 'red': 0, 'orange': 0}
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 0:
                counts['black'] += 1
            elif hue == 2 or hue == 3:
                counts['red'] += 1
            elif hue == 19 or hue == 20:
                counts['orange'] += 1
        if counts['black']>20 and counts['red']>10 and counts['orange']>5:
            return True
    if counts['black']>20 and counts['red']>10 and counts['orange']>5:
            return True
    return False

def processQG(xBounds, yBounds, pix):
    """blockProcess function to search for npc Quest Guide"""

    skin = 0
    green = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 17 or hue == 18:
                skin += 1
            elif hue == 93 or hue == 94:
                green += 1
        if skin > 15 and green > 15:
            return True
    if skin > 15 and green > 15:
        return True
    return False

def processLadder(xBounds, yBounds, pix):
    """blockProcess function to search for entity Ladder (near Quest Guide)"""

    black = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            p = pix[x,y]
            if p[0] == 0 and p[1] == 0 and p[2] == 0:
                black += 1
        if black > 20:
            return True
    return False

def processMI(xBounds, yBounds, pix):
    """blockProcess function to search for npc Mining Instructor"""

    purple = 0
    rune = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 132 or hue == 133:
                rune += 1
            elif hue == 197 or hue == 198:
                purple += 1
        if rune > 10 or purple > 20:
            return True
    if rune > 10 or purple > 20:   
        return True
    return False

def processTin(xBounds, yBounds, pix):
    """blockProcess function to search for entity Tin Rock"""

    tin = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 3 or hue == 4 or hue == 5:
                tin += 1
        if tin > 40:
            return True
    return False

def processCopper(xBounds, yBounds, pix):
    """blockProcess function to search for entity Copper Rock"""

    copper = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 17 or hue == 18:
                copper += 1
        if copper > 50:
            return True
    return False

def processFurnace(xBounds, yBounds, pix):
    """blockProcess function to search for entity Furnace"""

    furnace = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 0:
                furnace += 1
        if furnace > 100:
            return True
    return False

def processCI(xBounds, yBounds, pix):
    """blockProcess function to search for npc Combat Instructor"""

    hues = { 3: 0, 18: 0, 26: 0, }
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue in hues:
                hues[hue] += 1
        if hues[3] > 10 and hues[18] > 10 and hues[26] > 10:
            return True
    if hues[3] > 10 and hues[18] > 10 and hues[26] > 10:
        return True
    return False

def processRat(xBounds, yBounds, pix):
    """blockProcess function to search for entity Rat"""

    hues = { 36: 0, 40: 0, }
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue in hues:
                hues[hue] += 1
        if hues[36] > 10 and hues[40] > 20:
            return True
    if hues[36] > 10 and hues[40] > 20:
        return True
    return False

def processGate(xBounds, yBounds, pix):
    """blockProcess function to search for entity Gate"""

    wire = 0
    post = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 3 or hue == 4:
                post += 1
            elif hue == 0:
                wire += 1
        if wire > 20 and post > 10:
            return True
    if wire > 20 and post > 10:
        return True
    return False

def processLadderCave(xBounds, yBounds, pix):
    """blockProcess function to search for entity Ladder (in cave)"""

    lad = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 20 or hue == 22:
                lad += 1
        if lad > 40:
            return True
    if lad > 40:
        return True
    return False

def processFA(xBounds, yBounds, pix):
    """blockProcess function to search for npc Financial Advisor"""

    black = 0
    white = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            rgb = pix[x,y]
            if rgb[0] < 30 and rgb[1] < 30 and rgb[2] < 30:
                black += 1
            elif rgb[0] > 210 and rgb[1] > 210 and rgb[2] > 210:
                white += 1
        if black > 20 and white > 2:
            return True
    return False

def processBro(xBounds, yBounds, pix):
    """blockProcess function to search for npc Brother Bruce"""

    robe = 0
    hair = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 18 or hue == 19:
                robe += 1
            elif hue == 33:
                hair += 1
        if robe > 20 and hair > 1:
            return True
    return False

def processMag(xBounds, yBounds, pix):
    """blockProcess function to search for npc Magic Instructor"""

    hues = { 27: 0, 138: 0, }
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue in hues:
                hues[hue] += 1
        if hues[27] > 0 and hues[138] > 30:
            return True
    return False

def processChicken(xBounds, yBounds, pix):
    """blockProcess function to search for entity Chicken"""

    body = 0
    feet = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 25:
                body += 1
            elif hue == 32 or hue == 33:
                feet += 1
        if body > 10 and feet > 0:
            return True
    return False

def processBroDoor(xBounds, yBounds, pix):
    """blockProcess function to search for entity Door (leaving church)"""

    wood = 0
    for x in range(xBounds[0], xBounds[1]):
        for y in range(yBounds[0], yBounds[1]):
            hue = helpers.getHueFromRgb(pix[x,y])
            if hue == 26:
                wood += 1
        if wood > 85:
            return True
    return False


def catchOneFish(searchTimeLimit=30):
    """Catch one Shrimp"""
    
    # Get empty inv slot and inv item name to search for
    checkSlot = helpers.firstEmptyInvSlot()
    if checkSlot < 0:
        logging.info('Full inventory in catchOneFish')
        return False
    itemName = 'Raw shrimps'
    logging.info('Searching for ' + itemName + ' in slot ' + str(checkSlot))

    # Bbox for Fishing Spot
    tlcFish = helpers.coordsClientToPix((4, 4))
    brcFish = helpers.coordsClientToPix((516, 338))

    # Loop trying to fish until inv slot has Shrimp in it
    while True:
        # Locate and click fishing spot
        if not helpers.clickEntityDialog(
                bbox=(tlcFish[0], tlcFish[1], brcFish[0], brcFish[1]),
                blockProcess=processFishingSpot,
                option='net',
                name='Fishing spot',
                blockDimensions=(20,20)
                ):
            logging.info('Failed to find fishing spot after '
                         + str(searchTimeLimit) + ' seconds')
            return False
        
        # Wait until fish in inv slot or time expires
        start = time.time()
        while time.time() - start < 20:
            if helpers.isItemInSlot(itemName, checkSlot):
                logging.info('Found ' + itemName + '; returning')
                return True
            time.sleep(1)
        logging.info(itemName + ' not found in slot ' + str(checkSlot))


def makeFire():
    """Use log, tinderbox in inventory to make a fire"""
    
    while True:
        logging.info('Attempting to start fire...')
        tindSlot = helpers.searchInv('Tinderbox')
        logSlot = helpers.searchInv('Logs (tutorial)')
        helpers.clickInvSlot(tindSlot)
        time.sleep( random.uniform(0.05, 0.1) )
        helpers.clickInvSlot(logSlot)
        time.sleep(1.5)
        # Check that firemaking started by checking if log was removed from inv
        if not helpers.isInvSlotEmpty(logSlot):
            time.sleep( random.uniform(5, 8) )
            continue
        logging.info('Firemaking started')
        time.sleep(10)
        break


def cookOneFish():
    """Search for fire and use it to cook a shrimp"""

    # Bbox for Fire (whole view)
    tlcFire = helpers.coordsClientToPix((4, 4))
    brcFire = helpers.coordsClientToPix((516, 338))

    # Click first raw shrimps in inventory
    rawSlot = helpers.clickInvItem('Raw shrimps')
    if rawSlot < 0:
        logging.info('No raw shrimps in inventory in cookOneFish')
        return False

    # Locate and use with fire
    if not helpers.clickEntityDialog(
            bbox=(tlcFire[0], tlcFire[1], brcFire[0], brcFire[1]),
            blockProcess=processFire,
            option='usewith_Fire',
            name='Fire',
            blockDimensions=(15,15)
            ):
        logging.info('Failed to find fire in cookOneFish')
        return False

    # Wait until shrimp cooked or burnt
    time.sleep(5)
    start = time.time()
    while time.time() - start < 10:
        logging.info('Checking for Raw shrimps in slot ' + str(rawSlot))
        if not helpers.isItemInSlot('Raw shrimps', rawSlot):
            logging.info('Cooked shrimp. Returning')
            return True
        logging.info('Not cooking yet')
        time.sleep(1)
    if helpers.isItemInSlot('Raw shrimps', rawSlot):
        logging.info('Failed to cook shrimp in cookOneFish')
        return False
    return True


def killRat():
    """Locate rat, attack, return once rat is dead"""

    # Rat bbox
    tlcRat = helpers.coordsClientToPix( helpers.coordConsts['viewTlc'] )
    brcRat = helpers.coordsClientToPix( helpers.coordConsts['viewBrc'] )

    # Loop to start attacking
    logging.info('Locating rat to attack...')
    start = time.time()
    while time.time() - start < 30:
        if not helpers.clickNPCdialog(
                bbox=(tlcRat[0], tlcRat[1], brcRat[0], brcRat[1]),
                blockProcess=processRat,
                option='attack_Giant rat',
                name='Giant rat'
                ):
            return False
        logging.info('Clicked rat')
        time.sleep(4)
        pos = pag.locateCenterOnScreen('images\\tut_clicktocontinue.png')
        if not pos:
            logging.info('Attacking rat')
            break
    
    # Loop to wait until rat is dead
    while True:
        time.sleep(1.5)
        if ( pag.locateOnScreen('images\\tut_movingon.png') or
             pag.locateOnScreen('images\\tut_welldone.png') ):
            logging.info('Killed rat')
            return True
        logging.info('Still attacking...')



"""
Script
"""

def tutorial(clientName):
    """
    Script to complete tutorial island.
    Assume starting with a completely new character that was just logged in
    for the first time (so starting on character design screen).
    """
    startPAUSE = pag.PAUSE
    pag.PAUSE = 0
    helpers.focusClient(clientName)
    helpers.setHud()

    # Bounding box corners for entity searching:
    # Entire game view
    tlcEntire = helpers.coordsClientToPix( helpers.coordConsts['viewTlc'] )
    brcEntire = helpers.coordsClientToPix( helpers.coordConsts['viewBrc'] )
    # RuneScape Guide
    tlcRSG = helpers.coordsClientToPix((160, 57))
    brcRSG = helpers.coordsClientToPix((354, 282))
    # Door
    tlcDoor = helpers.coordsClientToPix((256, 4))
    brcDoor = helpers.coordsClientToPix((516, 338))
    # Survival Expert
    tlcSE = tlcEntire
    brcSE = brcEntire
    # Fishing spot
    tlcFish = helpers.coordsClientToPix((4, 256))
    brcFish = helpers.coordsClientToPix((516, 338))
    # Master Chef
    tlcChef = tlcEntire
    brcChef = brcEntire
    # Range
    tlcRange = helpers.coordsClientToPix((4, 256))
    brcRange = helpers.coordsClientToPix((516, 338))
    # Quest Guide's door
    tlcDoorQG = helpers.coordsClientToPix((144, 168))
    brcDoorQG = helpers.coordsClientToPix((409, 284))
    # Quest Guide
    tlcQG = tlcEntire
    brcQG = brcEntire
    # Ladder (near Quest Guide)
    tlcLad = helpers.coordsClientToPix((202, 118))
    brcLad = brcEntire
    # Mining Instructor
    tlcMI = tlcEntire
    brcMI = brcEntire
    # Tin rock
    tlcTin = tlcEntire
    brcTin = helpers.coordsClientToPix((256, 338))
    # Copper rock
    tlcCopper = helpers.coordsClientToPix((256, 4))
    brcCopper = brcEntire
    # Furnace
    tlcFurnace = helpers.coordsClientToPix((4, 167))
    brcFurnace = brcEntire
    # Anvil
    tlcAnvil = helpers.coordsClientToPix((4, 167))
    brcAnvil = brcEntire
    # Combat Instructor
    tlcCI = tlcEntire
    brcCI = brcEntire
    # Rat
    tlcRat = tlcEntire
    brcRat = brcEntire
    # Gate
    tlcGate = tlcEntire
    brcGate = brcEntire
    # Ladder (in cave)
    tlcLadCave = tlcEntire
    brcLadCave = brcEntire
    # Financial Advisor
    tlcFA = helpers.coordsClientToPix((245, 106))
    brcFA = helpers.coordsClientToPix((409, 198))
    # Brother Brace
    tlcBro = tlcEntire
    brcBro = helpers.coordsClientToPix((256, 338))
    # Brother Brace (later chats)
    tlcBro2 = (tlcEntire[0] + 100, tlcEntire[1])
    brcBro2 = brcEntire
    # Door (leaving Brother Brace)
    tlcBroDoor = helpers.coordsClientToPix((4, 220))
    brcBroDoor = brcEntire
    # Chicken
    tlcChicken = tlcEntire
    brcChicken = helpers.coordsClientToPix((516, 167))
    
    # Make random character
    designCharacter()
    
    # Set camera
    helpers.resetCamera()

    # Complete Runescape Guide tutorial part:
    # Click guide
    if not helpers.clickNPCdialog(
            bbox=(tlcRSG[0], tlcRSG[1], brcRSG[0], brcRSG[1]),
            blockProcess=processRunescapeGuide,
            option='talk-to',
            name='RuneScape Guide'
            ):
        return False
    # First chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]*7 +
        [{'type': 'choice', 'data': str(random.randint(1,3))}] +
        [{'type': 'continue'}]*3
        )
    
    # Click settings
    time.sleep( random.uniform(0.5, 1.5) )
    helpers.clickHud('tab_settings')
    
    # Turn music off, sounds lower
    time.sleep( random.uniform(0.5, 0.65) )
    helpers.clickHud('tab_settings_audio')
    time.sleep( random.uniform(0.3, 0.45) )
    helpers.clickHud('tab_settings_audio_music_0')
    time.sleep( random.uniform(0.3, 0.45) )
    helpers.clickHud('tab_settings_audio_effect_1')
    time.sleep( random.uniform(0.3, 0.45) )
    helpers.clickHud('tab_settings_audio_area_1')
    time.sleep( random.uniform(0.3, 0.45) )
    # Click guide
    if not helpers.clickNPCdialog(
            bbox=(tlcRSG[0], tlcRSG[1], brcRSG[0], brcRSG[1]),
            blockProcess=processRunescapeGuide,
            option='talk-to',
            name='RuneScape Guide'
            ):
        return False
    # Second chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )

    # Click door
    helpers.setRun('on')
    if not helpers.clickEntityDialog(
            bbox=(tlcDoor[0], tlcDoor[1], brcDoor[0], brcDoor[1]),
            blockProcess=processDoor,
            option='open',
            name='Door',
            blockDimensions=(20,40)
            ):
        return False
        
    

    # Run to Survival Expert
    time.sleep( random.uniform(2.5, 2.7) )
    helpers.clickMap(17, 45)
    

    # Complete Survival Expert tutorial part:
    # Click SE
    time.sleep( random.uniform(5.5, 6) )
    if not helpers.clickNPCdialog(
            bbox=(tlcSE[0], tlcSE[1], brcSE[0], brcSE[1]),
            blockProcess=processSurvivalExpert,
            option='talk-to',
            name='Survival Expert'
            ):
        return False
    # First chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    # Click inventory tab
    time.sleep( random.uniform(0.5, 1.5) )
    helpers.clickHud('tab_inventory')
    time.sleep( random.uniform(0.5, 0.6) )
    # Cut tree
    woodcutter.cutOneLog('Normal', tutorial=True)
    time.sleep( random.uniform(0.5, 1) )
    helpers.resetCamera()
    # Click SE
    if not helpers.clickNPCdialog(
            bbox=(tlcSE[0], tlcSE[1], brcSE[0], brcSE[1]),
            blockProcess=processSurvivalExpert,
            option='talk-to',
            name='Survival Expert'
            ):
        return False
    # Second chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]
        )
    
    # Make fire
    makeFire()
    # Clear 'you can't light...' chat block if necessary
    pos = pag.locateCenterOnScreen('images\\tut_clicktocontinue.png')
    if pos:
        mouseTo(pos[0], pos[1])
        time.sleep( random.uniform(0.1, 0.25) )
        pag.click()
    # Click skills tab
    time.sleep( random.uniform(0.5, 1.5) )
    helpers.clickHud('tab_skills')
    # Click SE
    if not helpers.clickNPCdialog(
            bbox=(tlcSE[0], tlcSE[1], brcSE[0], brcSE[1]),
            blockProcess=processSurvivalExpert,
            option='talk-to',
            name='Survival Expert'
            ):
        return False
    # Third chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    # Click inventory tab
    
    time.sleep( random.uniform(0.5, 1.5) )
    helpers.clickHud('tab_inventory')
    
    # Run to lake
    time.sleep( random.uniform(0.3, 0.5) )
    helpers.clickMapImage('images\\tut_compreflake.png')
    time.sleep ( random.uniform(4, 4.5) )
    # Net fishing spot
    catchOneFish()
    time.sleep ( random.uniform(2, 2.5) )
    
    # Cook shrimp (may need to chop tree and make fire)
    if True: #not cookOneFish():
        helpers.clickNeutral()
        time.sleep( random.uniform(0.3, 0.5) )
        woodcutter.cutOneLog('Normal', tutorial=True)
        makeFire()
        if not cookOneFish():
            logging.info('Failed to cook shrimp')
            return False
    time.sleep ( random.uniform(2, 2.5) )
    
    # Catch and cook shrimp again
    catchOneFish()
    time.sleep ( random.uniform(2, 2.5) )
    if not cookOneFish():
        helpers.clickNeutral()
        time.sleep( random.uniform(0.3, 0.5) )
        woodcutter.cutOneLog('Normal', tutorial=True)
        makeFire()
        if not cookOneFish():
            logging.info('Failed to cook shrimp')
            return False
    time.sleep ( random.uniform(2, 2.5) )
    # Run to gate
    if not helpers.clickMapImage('images\\tut_compref1.png', timeLimit=5):
        logging.info('Failed to navigate to gate')
        return False
    time.sleep( random.uniform(8, 8.15) )
    # Check for 'cancel' message
    pos = pag.locateCenterOnScreen('images\\tut_clicktocontinue.png')
    if pos:
        mouseTo(pos[0], pos[1])
        time.sleep( random.uniform(0.1, 0.2) )
        pag.click()
    
    # Click gate
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] - random.randint(14, 15), pos[1] - random.randint(2, 10))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click()
    time.sleep(2)

    
    # Run to chef's door
    if not helpers.clickMapImage('images\\tut_comprefCookDoor.png'):
        if not helpers.clickMapImage('images\\tut_comprefCookDoorBlocked.png'):
            logging.info('Failed to navigate to cook\'s door')
            return False
    time.sleep( random.uniform(8, 8.15) )
    
    # Click door
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] - random.randint(6, 8), pos[1] - random.randint(10, 11))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click()
    time.sleep(2)
    
    # Talk to chef
    if not helpers.clickNPCdialog(
            bbox=(tlcChef[0], tlcChef[1], brcChef[0], brcChef[1]),
            blockProcess=processChef,
            option='talk-to',
            name='Master Chef'
            ):
        return False
    
    # First chat
    time.sleep( random.uniform(1.5, 2) )
    helpers.chat(
        [{'type': 'continue'}]*5
        )
        
    # Use Pot of flour with Bucket of water
    helpers.useWithInv(names=('Pot of flour', 'Bucket of water'))
    
    
    # Cook Bread dough
    time.sleep( random.uniform(1, 1.15) )
    helpers.clickInvItem('Bread dough')
    if not helpers.clickEntityDialog(
            bbox=(tlcRange[0], tlcRange[1], brcRange[0], brcRange[1]),
            blockProcess=processRange,
            option='usewith_Range',
            name='Range',
            blockDimensions=(20,40)
            ):
        return False
    
    # Click music tab
    time.sleep( random.uniform(5, 6) )
    helpers.clickHud('tab_music')
    
    # Run to door
    time.sleep( random.uniform(0.25, 0.5) )
    helpers.clickMap(-10, -32)
    time.sleep( random.uniform(5, 5.5) )
    
    # Click door
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] - random.randint(12, 14), pos[1] - random.randint(0, 4))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click()
    time.sleep(2.5)
    # Click emotes tab
    helpers.clickHud('tab_emotes')
    # Click an emote
    time.sleep( random.uniform(0.3, 0.6) )
    emoteChoice = random.randint(0, 2)
    if emoteChoice == 0:
        helpers.clickHud('tab_emotes_shrug')
    elif emoteChoice == 1:
        helpers.clickHud('tab_emotes_laugh')
    elif emoteChoice == 2:
        helpers.clickHud('tab_emotes_jig')
    # Turn run on using settings tab
    time.sleep( random.uniform(2, 3) )
    helpers.clickHud('tab_settings')
    time.sleep( random.uniform(1, 1.5) )
    helpers.clickHud('tab_settings_run')
    
    # Run to Quest Guide
    helpers.clickMapDirection('n')
    time.sleep( random.uniform(7.4, 7.55) )
    helpers.clickMapDirection('n')
    time.sleep( random.uniform(6.9, 7.05) )
    
    helpers.clickMapDirection('e', 0.8)
    time.sleep( random.uniform(7.5, 7.65) )
    
    # Click door
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.25) )
    pag.click()
    time.sleep(2)
    
    # Click Quest Guide
    if not helpers.clickNPCdialog(
            bbox=(tlcQG[0], tlcQG[1], brcQG[0], brcQG[1]),
            blockProcess=processQG,
            option='talk-to',
            name='Quest Guide'
            ):
        return False
    time.sleep( random.uniform(2, 2.2) )
    # First chat
    helpers.chat(
        [{'type': 'continue'}]
        )
    time.sleep( random.uniform(0.5, 1) )
    
    helpers.clickHud('tab_quest')
    # Second chat
    time.sleep(2)
    if not helpers.clickNPCdialog(
            bbox=(tlcQG[0], tlcQG[1], brcQG[0], brcQG[1]),
            blockProcess=processQG,
            option='talk-to',
            name='Quest Guide'
            ):
        return False
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*5
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Climb down ladder
    if not helpers.clickEntityDialog(
            bbox=(tlcLad[0], tlcLad[1], brcLad[0], brcLad[1]),
            blockProcess=processLadder,
            option='climb-down',
            name='Ladder (Quest Guide)',
            blockDimensions=(30,20)
            ):
        helpers.clickMapDirection('se', 0.3)
        time.sleep( random.uniform(3.5, 3.65) )
        if not helpers.clickEntityDialog(
            bbox=(tlcLad[0], tlcLad[1], brcLad[0], brcLad[1]),
            blockProcess=processLadder,
            option='climb-down',
            name='Ladder (Quest Guide)',
            blockDimensions=(30,20)
            ):
            return False
    time.sleep( random.uniform(6, 6.5) )
    
    # Run to Mining Instructor
    helpers.clickMapDirection('sw')
    time.sleep( random.uniform(6, 6.15) )
    helpers.clickMapDirection('se', multiplier=0.7)
    time.sleep( random.uniform(4, 4.15) )
    
    # First chat
    if not helpers.clickNPCdialog(
            bbox=(tlcMI[0], tlcMI[1], brcMI[0], brcMI[1]),
            blockProcess=processMI,
            option='talk-to',
            name='Mining Instructor'
            ):
        return
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*3
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Prospect tin and copper
    if not helpers.clickEntityDialog(
            bbox=(tlcTin[0], tlcTin[1], brcTin[0], brcTin[1]),
            blockProcess=processTin,
            option='prospect',
            name='Tin Rock',
            blockDimensions=(25,25)
            ):
        return False
    time.sleep( random.uniform(10, 10.15) )
    
    helpers.clickMapDirection('e', 0.4)
    time.sleep( random.uniform(6, 6.15) )
    if not helpers.clickEntityDialog(
            bbox=(tlcCopper[0], tlcCopper[1], brcCopper[0], brcCopper[1]),
            blockProcess=processCopper,
            option='prospect',
            name='Copper Rock',
            blockDimensions=(25,25)
            ):
        return False
    time.sleep( random.uniform(10, 10.15) )
    helpers.clickMapDirection('w', 0.2)
    time.sleep( random.uniform(6, 6.15) )
    # Second chat
    if not helpers.clickNPCdialog(
            bbox=(tlcMI[0], tlcMI[1], brcMI[0], brcMI[1]),
            blockProcess=processMI,
            option='talk-to',
            name='Mining Instructor'
            ):
        return False
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*4
        )
    time.sleep( random.uniform(0.5, 1) )
    # Mine tin and copper
    if not helpers.clickEntityDialog(
            bbox=(tlcTin[0], tlcTin[1], brcTin[0], brcTin[1]),
            blockProcess=processTin,
            option='mine',
            name='Tin Rock',
            blockDimensions=(25,25)
            ):
        return False
    time.sleep( random.uniform(10, 10.15) )
    helpers.clickMapDirection('e', 0.4)
    time.sleep( random.uniform(6, 6.15) )
    if not helpers.clickEntityDialog(
            bbox=(tlcCopper[0], tlcCopper[1], brcCopper[0], brcCopper[1]),
            blockProcess=processCopper,
            option='mine',
            name='Copper Rock',
            blockDimensions=(25,25)
            ):
        return False
    time.sleep( random.uniform(10, 10.15) )
    helpers.clickMapDirection('w', 0.2)
    time.sleep( random.uniform(6, 6.15) )
    
    # Use copper with furnace to smelt
    helpers.clickHud('tab_inventory')
    time.sleep( random.uniform(0.25, 0.35) )
    helpers.clickInvItem('Copper ore')
    if not helpers.clickEntityDialog(
            bbox=(tlcFurnace[0], tlcFurnace[1], brcFurnace[0], brcFurnace[1]),
            blockProcess=processFurnace,
            option='usewith_Furnace',
            name='Furnace',
            blockDimensions=(60,20)
            ):
        return False
    time.sleep( random.uniform(8, 8.2) )
    # Click continue chat box
    helpers.clickButton('images\\tut_clicktocontinue.png')
    # Back to Mining Instructor
    helpers.clickMapDirection('n', multiplier=0.4)
    time.sleep( random.uniform(4, 4.15) )
    # Third chat
    if not helpers.clickNPCdialog(
            bbox=(tlcMI[0], tlcMI[1], brcMI[0], brcMI[1]),
            blockProcess=processMI,
            option='talk-to',
            name='Mining Instructor'
            ):
        return
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*3
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Click anvil
    helpers.clickMapDirection('sw')
    time.sleep( random.uniform(4, 4.15) )
    
    if not helpers.clickEntityDialog(
            bbox=(tlcAnvil[0], tlcAnvil[1], brcAnvil[0], brcAnvil[1]),
            blockProcess=processFurnace,
            option='smith',
            name='Anvil',
            blockDimensions=(20,20)
            ):
        return False
    time.sleep( random.uniform(4, 4.15) )
    # Smith bronze dagger
    helpers.clickButton('images\\tut_smithdagger.png')
    time.sleep( random.uniform(3, 3.15) )
    # Run to gate and open it
    helpers.clickMapDirection('ne', 0.7)
    time.sleep( random.uniform(5, 5.15) )
    
    if not helpers.clickMapImage('images\\tut_comprefCaveGate.png'):
        logging.info('Failed to navigate to cave gate')
        return False
    time.sleep( random.uniform(10, 10.15) )
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] + random.randint(14, 16), pos[1] - random.randint(0, 4))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click()
    time.sleep(2.5)
    
    # Run to Combat Instructor
    helpers.clickMapDirection('ne')
    time.sleep( random.uniform(6.5, 6.65) )
    
    # First chat: continue x3
    if not helpers.clickNPCdialog(
            bbox=(tlcCI[0], tlcCI[1], brcCI[0], brcCI[1]),
            blockProcess=processCI,
            option='talk-to',
            name='Combat Instructor'
            ):
        return False
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*3
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click equipment tab
    helpers.clickHud('tab_equipment')
    time.sleep( random.uniform(0.5, 1) )
    
    # Click view equipment stats
    helpers.clickHud('tab_equipment_stats')
    time.sleep( random.uniform(0.5, 1) )
    
    # Click bronze dagger to equip
    print(helpers.clickInvItem('Bronze dagger (equip)'))
    time.sleep( random.uniform(0.5, 1) )
    helpers.clickButton('images\\tut_closeviewbutton.png')
    
    # Second chat: continue x2
    if not helpers.clickNPCdialog(
            bbox=(tlcCI[0], tlcCI[1], brcCI[0], brcCI[1]),
            blockProcess=processCI,
            option='talk-to',
            name='Combat Instructor'
            ):
        return False
    time.sleep( random.uniform(2, 2.2) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click inventory
    helpers.clickHud('tab_inventory')
    time.sleep( random.uniform(0.5, 1) )
    # Click bronze sword and wooden shield
    helpers.clickInvItem('Bronze sword')
    time.sleep( random.uniform(0.2, 0.4) )
    helpers.clickInvItem('Wooden shield')
    time.sleep( random.uniform(1.5, 1.6) )
    
    # Click combat tab
    helpers.clickHud('tab_combat')
    time.sleep( random.uniform(0.5, 1) )
    
    # Run to rat gate and open it
    helpers.clickMapImage('images\\tut_comprefRatWall.png')
    time.sleep( random.uniform(7.5, 7.65) )
    if not helpers.clickEntityDialog(
            bbox=(tlcGate[0], tlcGate[1], brcGate[0], brcGate[1]),
            blockProcess=processGate,
            option='open',
            name='Gate',
            blockDimensions=(10,30)
            ):
        return False
    time.sleep( random.uniform(4, 4.15) )
    # Kill a rat
    killRat()
    
    # Open rat gate
    helpers.clickMapDirection('e')
    time.sleep( random.uniform(7.5, 7.65) )
    if not helpers.clickEntityDialog(
            bbox=(tlcGate[0], tlcGate[1], brcGate[0], brcGate[1]),
            blockProcess=processGate,
            option='open',
            name='Gate',
            blockDimensions=(10,30)
            ):
        return False
    time.sleep( random.uniform(7, 7.15) )
    # Run to Combat Instructor
    helpers.clickMapDirection('s', 0.7)
    time.sleep( random.uniform(7, 7.15) )
    # Third chat: continue x4
    if not helpers.clickNPCdialog(
            bbox=(tlcCI[0], tlcCI[1], brcCI[0], brcCI[1]),
            blockProcess=processCI,
            option='talk-to',
            name='Combat Instructor'
            ):
        return False
    time.sleep( random.uniform(5, 5.2) )
    helpers.chat(
        [{'type': 'continue'}]*4
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click inventory tab
    helpers.clickHud('tab_inventory')
    time.sleep( random.uniform(0.5, 1) )
    # Click shortbow and bronze arrow
    helpers.clickInvItem('Shortbow')
    time.sleep( random.uniform(0.2, 0.3) )
    
    helpers.clickInvItem('Bronze arrow', numbered=True)
    time.sleep( random.uniform(0.2, 0.3) )
    # Attack rat and wait for kill (ranging)
    helpers.clickMapDirection('ne')
    time.sleep( random.uniform(6.5, 6.65) )
    killRat()
    
    # Run to ladder and climb up
    helpers.clickMapDirection('ne')
    time.sleep( random.uniform(7.5, 7.65) )
    # Reset camera
    helpers.resetCamera()
    
    if not helpers.clickEntityDialog(
            bbox=(tlcLadCave[0], tlcLadCave[1], brcLadCave[0], brcLadCave[1]),
            blockProcess=processLadderCave,
            option='climb-up',
            name='Gate',
            blockDimensions=(20,20)
            ):
        return False
    time.sleep( random.uniform(10, 10.2) )
    
    # Run to Banker
    helpers.clickMapImage('images\\tut_comprefBank.png')
    time.sleep( random.uniform(10, 10.2) )
    
    # Chat: continue, chat option 1
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] + random.randint(-2, 2), pos[1] - random.randint(50, 51))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click(button='right')
    time.sleep( random.uniform(0.2, 0.25) )
    if not pag.locateOnScreen('images\\dialog_talk-to.png'):
        mouseTo(pos[0] + random.randint(2, 4), pos[1] - random.randint(24, 26))
        time.sleep ( random.uniform(0.05, 0.15) )
        pos = (pos[0] + random.randint(25, 26), pos[1] - random.randint(0, 1))
        mouseTo(pos[0], pos[1], precise=True)
        time.sleep( random.uniform(0.1, 0.2) )
        pag.click(button='right')
        time.sleep( random.uniform(0.2, 0.25) )
        if not pag.locateOnScreen('images\\dialog_talk-to.png'):
            logging.info('Failed to locate Banker')
            return False
    helpers.clickButton('images\\dialog_talk-to.png')
    time.sleep( random.uniform(1.5, 1.65) )
    helpers.chat(
        [{'type': 'continue'}] +
        [{'type': 'choice', 'data': '1'}]
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click close view
    helpers.clickButton('images\\tut_closeviewbutton.png')
    time.sleep( random.uniform(0.3, 0.5) )
    
    # Click use poll booth
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] - random.randint(34, 35), pos[1] + random.randint(43, 44))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.1, 0.2) )
    pag.click(button='right')
    time.sleep( random.uniform(0.2, 0.25) )
    if not pag.locateOnScreen('images\\dialog_use.png'):
        mouseTo(pos[0] + random.randint(2, 4), pos[1] - random.randint(24, 26))
        time.sleep ( random.uniform(0.05, 0.15) )
        pos = (pos[0] - random.randint(25, 26), pos[1] + random.randint(0, 1))
        mouseTo(pos[0], pos[1], precise=True)
        time.sleep( random.uniform(0.1, 0.2) )
        pag.click(button='right')
        time.sleep( random.uniform(0.2, 0.25) )
        if not pag.locateOnScreen('images\\dialog_use.png'):
            logging.info('Failed to locate Poll Booth')
            return False
    helpers.clickButton('images\\dialog_use.png')
    time.sleep( random.uniform(3.5, 3.65) )
    helpers.chat(
        [{'type': 'continue'}]*3
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click close view
    helpers.clickButton('images\\tut_closeviewbutton.png')
    time.sleep( random.uniform(0.3, 0.5) )
    
    # Open door
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] + random.randint(124, 125), pos[1] - random.randint(83, 84))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.05, 0.15) )
    pag.click()
    time.sleep( random.uniform(7, 7.15) )
    
    # Talk to Financial Advisor
    # Chat: continue x9
    if not helpers.clickNPCdialog(
            bbox=(tlcFA[0], tlcFA[1], brcFA[0], brcFA[1]),
            blockProcess=processFA,
            option='talk-to',
            name='Financial Advisor'
            ):
        return False
    time.sleep( random.uniform(3, 3.15) )
    
    helpers.chat(
        [{'type': 'continue'}]*9
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Open door (can use entity searching on right half of screen)
    if not helpers.clickEntityDialog(
            bbox=(tlcDoor[0], tlcDoor[1], brcDoor[0], brcDoor[1]),
            blockProcess=processDoor,
            option='open',
            name='Door',
            blockDimensions=(20,40)
            ):
        return False
    time.sleep( random.uniform(4.5, 4.65) )
    
    # Run to church, open door if necessary
    helpers.clickMapDirection('s')
    time.sleep( random.uniform(9, 9.15) )
    
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] - random.randint(40, 41), pos[1] + random.randint(5, 6))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.05, 0.15) )
    pag.click(button='right')
    time.sleep(0.25)
    pos = pag.locateCenterOnScreen('images\\dialog_open.png')
    if pos:
        mouseTo(pos[0], pos[1], precise=True)
        time.sleep( random.uniform(0.05, 0.15) )
        pag.click()
        time.sleep( random.uniform(3.5, 3.65) )
        pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
        pos = (pos[0] - random.randint(24, 25), pos[1] + random.randint(10, 11))
        mouseTo(pos[0], pos[1], precise=True)
        time.sleep( random.uniform(0.05, 0.15) )
        pag.click()
        time.sleep(2.5)
        
    # Talk to Brother Brace
    # Chat: continue x2
    if not helpers.clickNPCdialog(
            bbox=(tlcBro[0], tlcBro[1], brcBro[0], brcBro[1]),
            blockProcess=processBro,
            option='talk-to',
            name='Brother Brace'
            ):
        return False
    time.sleep( random.uniform(4.5, 4.65) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click prayer tab
    helpers.clickHud('tab_prayer')
    time.sleep( random.uniform(0.3, 0.5) )
    
    # Chat: continue x4
    if not helpers.clickNPCdialog(
            bbox=(tlcBro2[0], tlcBro2[1], brcBro2[0], brcBro2[1]),
            blockProcess=processBro,
            option='talk-to',
            name='Brother Brace'
            ):
        return False
    time.sleep( random.uniform(2.5, 2.65) )
    helpers.chat(
        [{'type': 'continue'}]*4
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click friends tab, click ignore tab
    helpers.clickHud('tab_friends')
    time.sleep( random.uniform(0.3, 0.5) )
    helpers.clickHud('tab_ignore')
    time.sleep( random.uniform(0.3, 0.5) )
    
    # Chat: continue x8
    if not helpers.clickNPCdialog(
            bbox=(tlcBro2[0], tlcBro2[1], brcBro2[0], brcBro2[1]),
            blockProcess=processBro,
            option='talk-to',
            name='Brother Brace'
            ):
        return
    time.sleep( random.uniform(2.5, 2.65) )
    helpers.chat(
        [{'type': 'continue'}]*8
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Reset camera
    helpers.resetCamera()
    
    # Open door
    helpers.clickMapImage('images\\tut_comprefBro.png')
    time.sleep( random.uniform(4.5, 4.65) )
    pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
    pos = (pos[0] + random.randint(25, 26), pos[1] + random.randint(10, 11))
    mouseTo(pos[0], pos[1], precise=True)
    time.sleep( random.uniform(0.05, 0.15) )
    pag.click(button='right')
    time.sleep( random.uniform(0.3, 0.45) )
    try:
        helpers.clickButton('images\\dialog_open.png')
    except:
        pos = pag.position()
        pos = (pos[0] + random.randint(-2, 2), pos[1] - random.randint(18, 20))
        mouseTo(pos[0], pos[1])
        pos = helpers.coordsClientToPix(helpers.coordConsts['viewCenter'])
        pos = (pos[0] + random.randint(0, 2), pos[1] + random.randint(10, 11))
        mouseTo(pos[0], pos[1], precise=True)
        time.sleep( random.uniform(0.05, 0.15) )
        pag.click(button='right')
        time.sleep( random.uniform(0.3, 0.45) )
        helpers.clickButton('images\\dialog_open.png')
    time.sleep( random.uniform(2.2, 2.3) )
    
    # Run to Magic Instructor
    helpers.clickMapDirection('se')
    time.sleep( random.uniform(8, 8.15) )
    
    helpers.clickMapDirection('se', 0.85)
    time.sleep( random.uniform(8, 8.15) )
    
    # Talk to Magic Instructor
    # Chat: continue x2
    if not helpers.clickNPCdialog(
            bbox=(tlcEntire[0], tlcEntire[1], brcEntire[0], brcEntire[1]),
            blockProcess=processMag,
            option='talk-to',
            name='Magic Instructor'
            ):
        return False
    time.sleep( random.uniform(3.5, 3.65) )
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    time.sleep( random.uniform(0.5, 1) )
    # Click magic tab
    
    helpers.clickHud('tab_magic')
    time.sleep( random.uniform(0.3, 0.5) )
    # Chat: continue x2 (NOTE: do NOT need to click magic instructor, chat
    #   starts automatically)
    helpers.chat(
        [{'type': 'continue'}]*2
        )
    time.sleep( random.uniform(0.5, 1) )
    
    # Move to chickens
    helpers.clickMapImage('images\\tut_comprefChicken.png')
    time.sleep( random.uniform(4, 4.15) )
    # Click Wind Strike, then right-click cast on Chicken
    helpers.clickHud('tab_magic_windstrike')
    time.sleep( random.uniform(0.2, 0.35) )
    if not helpers.clickEntityDialog(
            bbox=(tlcChicken[0], tlcChicken[1], brcChicken[0], brcChicken[1]),
            blockProcess=processChicken,
            option='cast_Chicken',
            name='Chicken',
            blockDimensions=(20,20)
            ):
        return False
    time.sleep( random.uniform(4.5, 4.65) )
    
    # If blocked (ran to wrong place)...
    if pag.locateOnScreen('images\\tut_clicktocontinue.png'):
        helpers.clickButton('images\\tut_clicktocontinue.png')
        time.sleep( random.uniform(0.3, 0.4) )
        helpers.clickMapImage('images\\tut_comprefChicken.png')
        time.sleep( random.uniform(8, 8.15) )
        # Try to wind strike chicken again
        helpers.clickHud('tab_magic_windstrike')
        time.sleep( random.uniform(0.2, 0.35) )
        if not helpers.clickEntityDialog(
                bbox=(tlcChicken[0], tlcChicken[1], brcChicken[0], brcChicken[1]),
                blockProcess=processChicken,
                option='cast_Chicken',
                name='Chicken',
                blockDimensions=(20,20)
                ):
            return False
        time.sleep( random.uniform(4.5, 4.65) )
        
    
    # Chat: continue, chat option 1, continue, chat option 2, continue x6
    if not helpers.clickNPCdialog(
            bbox=(tlcEntire[0], tlcEntire[1], brcEntire[0], brcEntire[1]),
            blockProcess=processMag,
            option='talk-to',
            name='Magic Instructor'
            ):
        return False
    time.sleep( random.uniform(2.5, 2.65) )
    helpers.chat(
        [{'type': 'continue'}] +
        [{'type': 'choice', 'data': '1'}] +
        [{'type': 'continue'}] +
        [{'type': 'choice', 'data': '2'}] +
        [{'type': 'continue'}]*6
        )
    time.sleep( random.uniform(4, 4.15) )
    # Wait then chat: continue to clear chat box
    
    helpers.chat(
        [{'type': 'continue'}]
        )
    
    pag.PAUSE = startPAUSE
    return True
    
    
    





"""
Testing script
"""
## 0 - use first 'tutorial' account
## 1 - use first 'new' account or make new
## 2 - run without logging in
## anything else - do nothing
getAccount = 3

if getAccount == 0: ## Use 'tutorial' account from private_accounts
    # Get first 'tutorial' account
    from private_accounts import accounts
    account = None
    for acc in accounts:
        if acc['status'] == 'tutorial':
            account = acc
            break
    if account:
        creds = account['credentials']
    else:
        print('Failed to find an account with \'tutorial\' status')

    # Login and run tutorial
    clientName = 'Old School RuneScape'
    worlds = helpers.f2pWorlds
    world = worlds[ random.randint(0, len(worlds)-1) ]
    helpers.focusClient(clientName)
    helpers.login(creds[0], creds[1], world, tutorial=True)

    if tutorial(clientName):
        # Update account status in private_accounts
        if helpers.updateAccountStatus(creds[0], creds[1], 'done tutorial'):
            logging.info('Updated account status to: done tutorial')
        
elif getAccount == 1: ## Use 'new' account or make new account
    # Get first 'new' account
    from private_accounts import accounts
    account = None
    for acc in accounts:
        if acc['status'] == 'new':
            account = acc
            break
    if account:
        creds = account['credentials']
    else:
        from makeAccount import makeAccount
        creds = makeAccount()

    # Login and run tutorial
    clientName = 'Old School RuneScape'
    worlds = helpers.f2pWorlds
    world = worlds[ random.randint(0, len(worlds)-1) ]
    helpers.focusClient(clientName)
    helpers.login(creds[0], creds[1], world, tutorial=True)

    if tutorial(clientName):
        # Update account status in private_accounts
        if helpers.updateAccountStatus(creds[0], creds[1], 'done tutorial'):
            logging.info('Updated account status to: done tutorial')
        
elif getAccount == 2: ## Just run tutorial
    tutorial('Old School RuneScape')



