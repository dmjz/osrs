#! python3

"""
Running scripts
"""

import random
from private_accounts import accounts
from woodcutter import woodcutter
from makeAccount import makeAccount
from tutorial import tutorial
from startAccount import startAccount
import loginInfo
import helpers


"""
Note: generally, functions assume a running instance of the OSRS client.
"""

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


def tutorialIsland():
    """
    Select a new account from private_accounts (or create new account),
    log in and complete tutorial island.
    """

    # Client options
    clientName = loginInfo.clientName
    clientPath = loginInfo.clientPath

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
        if not helpers.updateAccountStatus(creds[0], creds[1], 'tutorial'):
            logging.info('Failed to update account status; exiting')
            return False
    else:
        logging.info('Failed to log in; exiting')
        return False

    # Complete tutorial island
    tutorial(clientName=clientName)



tutorialIsland()




    
