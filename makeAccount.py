#! python3

"""
Create a new OSRS account and record its data in private_accounts.py.
"""

import os
import sys
import logging
import time
import random
import pprint
import pywinauto
from pywinauto.application import Application
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
import pyautogui as pag
from mouseMoveFunction import mouseTo
import helpers
from generateLists import lists
from private_accounts import accounts

pag.PAUSE = 0


def genAccountData():
    """Return randomly generated tuple: (email, password, display name)"""

    # Generate email
    adjList = lists['adjectives']
    nameList = lists['names']

    adj = adjList[random.randint( 0, len(adjList)-1 )]
    name = nameList[random.randint( 0, len(nameList)-1 )]
    if random.randint(0, 1) == 0:
        num = str(random.randint(10, 99))
    else:
        num = str(random.randint(1910, 2100))
    tail = '@mail.com'

    adjFirst = random.randint(0, 1)
    numMiddle = random.randint(0, 1)

    if adjFirst == 1 and numMiddle == 1:
        parts = [adj, num, name, tail]
    if adjFirst == 1 and numMiddle == 0:
        parts = [adj, name, num, tail]
    if adjFirst == 0 and numMiddle == 1:
        parts = [name, num, adj, tail]
    if adjFirst == 0 and numMiddle == 0:
        parts = [name, adj, num, tail]

    email = ''.join(parts)
    
    # Generate password
    alpha = 'qwaszxerdfcvtyghbnuijkmolpQWASZXERDFCVTYGHBNUIJKMOLP'

    parts = []
    for i in range(random.randint(10,12)):
        if random.randint(0, 2) == 0:
            parts.append( str(random.randint(0,9)) )
        else:
            parts.append( alpha[random.randint(0, 51)] )

    password = ''.join(parts)

    # Generate display name    
    consonants = 'bcdfghjklmnpqrstvwxyz'
    doubleCons = ['ch', 'th', 'wh', 'ck', 'sh', 'cr', 'tt', 'nn', 'mm',
                  'st', 'ss', 'rr', 'kk']
    allCons = doubleCons + list(consonants)
    vowels = 'aeiouy'
    doubleVows = ['ee', 'oo', 'ue', 'eu', 'oa', 'au']
    allVows = doubleVows + list(vowels)
    chunks = ['oof', 'arm', 'art', 'ark', 'pop', 'mot', 'plot', 'far', 'ram',
              'rom', 'rim', 'rum', 'urn', 'urk', 'ert', 'erk', 'ork', 'orn',
              'nut', 'num', 'nun', 'nop', 'nip', 'nap', 'net', 'fun', 'fan',
              'lot', 'cra', 'car', 'cur', 'cup', 'cut', 'zap', 'zip', 'zam',
              'goo', 'got', 'goy', 'gut', 'gal', 'gak', 'gar', 'gre', 'gap']

    while True:
        parts = []
        numFlag = random.randint(0, 3)
        numChoice = str(random.randint(0,99))
        if numFlag == 1 or numFlag == 2:
            parts.append( numChoice )
        for i in range(random.randint(3, 6)):
            choice = random.randint(1, 5)
            if choice == 1: # consonant plus vowel
                parts.append( allCons[random.randint(0, len(allCons)-1)] )
                parts.append( allVows[random.randint(0, len(allVows)-1)] )
            if choice == 2: # vowel plus consonant
                parts.append( allVows[random.randint(0, len(allVows)-1)] )
                parts.append( allCons[random.randint(0, len(allCons)-1)] )
            if choice == 3: # name
                parts.append( nameList[random.randint(0, len(nameList)-1)] )
                if random.randint(0, 2) == 0:
                    parts.append(' ')
            if choice == 4: # adjective
                parts.append( adjList[random.randint(0, len(adjList)-1)] )
                if random.randint(0, 2) == 0:
                    parts.append(' ')
            if choice == 5: # chunk
                parts.append( chunks[random.randint(0, len(chunks)-1)] )
                if random.randint(0, 2) == 0:
                    parts.append(' ')
        if numFlag == 2 or numFlag == 3:
            parts.append( numChoice )
            
        name = ''.join(parts)
        
        # Verify name is not too long
        if len(name) > 12:
            continue
        # Verify name is not all numbers
        allNums = True
        for c in name:
            if not c in '0123456789':
                allNums = False
                break
        if allNums:
            continue

        # If name passed verification, break
        break

    return (email, password, name)


            
#----------------------------------------------------------------------
"""
Script
"""

def makeAccount():
    """
    Create a new OSRS account with random account data and return a 3-tuple:
        (email, password, display name)
    and write the new account credentials to private_accounts.py
    Return False if account creation fails. 
    """
    
    #
    # TODO: remove as much screen searching as possible. This seems
    # to break rapidly and is a total goober way to do it anyway.
    #
    
    # Start browser
    browserPath = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    browser = Application(backend='uia').start(browserPath)
    
    # Navigate to OSRS account creation page
    helpers.typeString('https://oldschool.runescape.com/')
    pag.press('enter')
    start = time.time()
    while not pag.locateCenterOnScreen(helpers.images['signupbutton2']):
        time.sleep(0.5)
        if time.time() - start > 5:
            pag.press('right')
            time.sleep(0.2)
            pag.press('right')
            time.sleep(0.2)
            pag.press('right')
            time.sleep(0.2)
            pag.press('right')
            time.sleep(0.2)
            start = time.time()
            while not pag.locateCenterOnScreen(helpers.images['signupbutton2']):
                time.sleep(0.5)
                if time.time() - start > 5:
                    start = time.time()
                    logging.info('Could not locate signupbutton image')
                    return False
    helpers.clickButton(helpers.images['signupbutton2'])
    start = time.time()
    while not pag.locateCenterOnScreen(helpers.images['createaccount']):
        time.sleep(0.5)
        if time.time() - start > 5:
            logging.info('Could not locate createaccount image')
            return False

    # Enter form data
    email, password, name = genAccountData()
    day = str(random.randint(1,25))
    month = str(random.randint(1,12))
    year = str(random.randint(1980, 1999))

    helpers.typeString(email)
    pag.press('tab')
    helpers.typeString(password)
    pag.press('tab')
    helpers.typeString(name)
    pag.press('tab')
    helpers.typeString(day)
    pag.press('tab')
    helpers.typeString(month)
    pag.press('tab')
    helpers.typeString(year)

    # Click Captcha, submit, wait for confirmation, then close browser
    pag.scroll(random.randint(-1000, -800))
    time.sleep(0.5)
    helpers.clickButton(helpers.images['captchabox'])
    time.sleep(2)
    if pag.locateCenterOnScreen(helpers.images['submitcreate']):
        helpers.clickButton(helpers.images['submitcreate'])
    else:
        pos = pag.position()
        pos = (pos[0] + 108, pos[1] + 156)
        mouseTo(pos[0], pos[1])
        pag.click()
    start = time.time()
    while not pag.locateCenterOnScreen(helpers.images['confirmcreate']):
        time.sleep(1)
        if time.time() - start > 30:
            logging.info('Could not locate confirmcreate')
            return False
    helpers.clickButton(helpers.images['confirmcreate'])
    pag.keyDown('alt')
    pag.press('f4')
    pag.keyUp('alt')
    browser.kill()

    # Record account data
    accounts.append({
        'credentials': (email, password, name),
        'status': 'new',
        })
    file = open('private_accounts.py', 'w')
    file.write('accounts = ' + pprint.pformat(accounts))
    file.close()

    # Return account data
    return (email, password, name)


