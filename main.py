#! python3

"""
This file contains some scripts intended to be run at the top-level 
(i.e. outside of any called functions from the osrs library). 
Instructions to run:
  0. Start your OSRS client
  1. Start a command shell
  2. Activate the osrs_test virtual environment
  3. Start a Python shell
  4. Import main
  5. Call whatever function from main that you'd like to run,
       e.g. tutorialIsland()
       
Note: generally, functions assume a running instance of the OSRS client.
"""

import random
import logging
from private_accounts import accounts
from woodcutter import woodcutter
from makeAccount import makeAccount
from tutorial import tutorial
from startAccount import startAccount
import loginInfo
import helpers


# woodcutter default options
defaultOptions = { 'treetype': 'Normal', 'bank': False }
defaultEndOptions = { 'condition': 'num', 'data': 10 }

def startWoodcutter(options=defaultOptions, endOptions=defaultEndOptions):
    """
    Start woodcutter using my client and options and an account
    from private_accounts.
    """

    # Client info
    clientName = loginInfo.clientName
    clientPath = loginInfo.clientPath
    
    # Get first account that's ready for woodcutting
    for acc in accounts:
        if acc['status'] == 'done tutorial':
            account = acc
            break
    creds = account['credentials']

    # Start client and login
    #helpers.startClient(clientName, clientPath)
    ## Note: can't figure out a way to start Jagex client because you have to
    ## use the shortcut, not the executable.
    worlds = helpers.f2pWorlds
    world = worlds[ random.randint(0, len(worlds)-1) ]
    helpers.focusClient(clientName)
    helpers.login(username=creds[0], password=creds[1], world=world)

    # Start woodcutter
    wcReturn = woodcutter(options=options, clientName=clientName,
                          endOptions=endOptions)
    if wcReturn:
        logging.info('Woodcutter return: ' + wcReturn)
    else:
        logging.info('Woodcutter exited without return value')
        
        
def makeAndStoreAccount():
    """
    Make an account and store credentials in private_accounts
    """
    
    creds = makeAccount()
    if not creds:
        logging.info('makeAccount failed; exiting')
        return False
    logging.info('makeAccount returned credentials:\n' + str(creds))
    return True


def tutorialIsland(accountCreds=None):
    """
    Select a new account from private_accounts.py (or create new account),
    log in and complete tutorial island.
    To use your own account credentials, pass them as accountCreds.
      Format: (email, password, display name)
    (display name is optional here)
    But note: these will not be stored in private_accounts.py, and status
    will not be maintained by the osrs library.
    """

    # Client options
    clientName = loginInfo.clientName
    clientPath = loginInfo.clientPath
    
    # Use accountCreds as credentials, if passed
    if accountCreds:
        print('Using user credentials')
        creds = accountCreds
    else:
    # Get first new account, or make one
        account = None
        for acc in accounts:
            if acc['status'] == 'new':
                account = acc
                break
        if account:
            creds = account['credentials']
        else:
            creds = makeAccount()
            if not creds:
                logging.info('Could not find or create new account; exiting')
                return False

    # Log in
    worlds = helpers.f2pWorlds
    world = worlds[ random.randint(0, len(worlds)-1) ]
    helpers.focusClient(clientName)
    if helpers.login(creds[0], creds[1], world, tutorial=True):
        if not accountCreds:
            if not helpers.updateAccountStatus(creds[0], creds[1], 'tutorial'):
                logging.info('Failed to update account status; exiting')
                return False
    else:
        logging.info('Failed to log in; exiting')
        return False

    # Complete tutorial island
    print('Launching tutorial')
    tutorial(clientName=clientName)
    

def runStartAccount(creds, supplies=None, setup=True, travel=True, buySupplies=True):
    # Default supplies if None passed
    if not supplies and buySupplies:
        supplies = [
            {'item': 'Mithril axe', 'quantity': 1, 'price': 5020},
            {'item': 'Rune axe', 'quantity': 1, 'price': 10103}
            ]
            
    clientName = 'Old School RuneScape'
    worlds = helpers.f2pWorlds
    world = worlds[ random.randint(1, len(worlds)-1) ] #any world except 1
    helpers.focusClient(clientName)
    helpers.login(creds[0], creds[1], world, tutorial=False)
    startAccount(
        clientName,
        supplies=supplies,
        setup=setup,
        travel=travel,
        buySupplies=buySupplies
        )




    
