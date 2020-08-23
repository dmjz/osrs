#! python3

"""
Take an account that just finished tutorial island, get him to the GE, and
chop and sell logs until he can afford a list of supplies.
"""

import time
import random
import logging
import pyautogui as pag
from PIL import ImageGrab
from PIL import Image
from private_accounts import accounts
from woodcutter import woodcutter
import loginInfo
import helpers

logging.getLogger().setLevel(logging.INFO)

"""
Functions and variables
"""

def verifyStartLoc():
    """Verify starting at (roughly) the Tutorial Island exit location"""

    for i in range(1, 4):
        if helpers.searchMapImage(
                'images\\start_comprefInit' + str(i) + '.png',
                timeLimit=5
                ):
            return True
    return False


def travelTutExitToGEForest():
    """Walk from Tutorial Island exit spot to forest south of GE"""
    
    if not verifyStartLoc():
        logging.info('Failed to verify starting location')
        return False

    logging.info('Starting: tutorial island exit spot')
    helpers.setRun('off')
    helpers.walkSeries(['n', 'n', 'nw', 'nw', 'w', 'nw', 'w'])
    time.sleep( random.uniform(3, 3.1) )
    if not helpers.clickMapImage('images\\start_comprefMill.png'):
        logging.info('Got lost before mill')
        return False
    time.sleep( random.uniform(9, 9.1) )
    logging.info('Checkpoint: entrance of mill')
    helpers.walkSeries(['nw', 'nw', 'n', 'n'])
    logging.info('Moving east to avoid hostile tree')
    helpers.clickMapDirection('e', 0.1)
    time.sleep( random.uniform(3, 3.1) )
    helpers.clickMapDirection('n')
    time.sleep( random.uniform(10.5, 10.6) )
    logging.info('Checkpoint: dead tree field east of mansion')
    helpers.walkSeries(['e', 'n', 'n'])
    logging.info('Checkpoint: past bottleneck between river and mansion')
    helpers.walkSeries(['nw', 'n'])
    if not helpers.clickMapImage('images\\start_comprefBarbBridge.png'):
        logging.info('Got lost before bridge east of Barb Village')
        return False
    time.sleep( random.uniform(10.5, 10.6) )
    logging.info('Checkpoint: bridge from Barb Village to west of Varrock')
    helpers.walkSeries(['ne']*5)
    time.sleep( random.uniform(3, 3.1) )
    if not helpers.searchMapImage('images\\start_comprefGEcorner.png'):
        logging.info('Failed to navigate to forest south of GE')
        return False
    logging.info('Arrived: forest south of GE')
    helpers.clickMapDirection('s', 0.7)
    time.sleep( random.uniform(7.5, 7.6) )
    return True


# List of items to clear from inventory
wcClearList = [
        'Tinderbox', 'Small fishing net', 'Shrimps', 'Bucket',
        'Pot', 'Bread', 'Bronze pickaxe', 'Bronze dagger',
        'Bronze sword', 'Wooden shield', 'Shortbow', 'Bronze arrow',
        'Air rune', 'Mind rune', 'Water rune', 'Earth rune',
        'Body rune'
    ]


"""
Script
"""

def startAccount(clientName, supplies, itemClearList=wcClearList,
                 setup=False, travel=False, buySupplies=True):
    """
    Script to get starting supplies for an account fresh off of tutorial
    island. Will travel to GE, cut and sell normal logs, and purchase a
    list of supplies.

    Assume account is logged in and character standing at tutorial exit spot.
    """
    print('startAccount called:')
    print(str({'setup':setup, 'travel':travel, 'buySupplies':buySupplies}))
    
    # 0. Initialize
    startPAUSE = pag.PAUSE
    pag.PAUSE = 0
    helpers.focusClient(clientName)
    helpers.setHud()
    helpers.setGE()
    helpers.resetCamera()
    
    # 1. Set up inventory, options.
    if setup:
        helpers.clickHud('tab_settings')
        time.sleep( random.uniform(1, 1.15) )
        helpers.clickHud('tab_settings_controls')
        time.sleep( random.uniform(0.6, 0.7) )
        pos = pag.locateOnScreen('images\\shiftdrop_on.png')
        if not pos:
            ###
            ### Shift-click button locations has changed
            ###
            helpers.clickHud('tab_settings_controls_shiftclick')
            time.sleep( random.uniform(0.3, 0.4) )
        helpers.clickHud('tab_inventory')
        time.sleep( random.uniform(0.5, 0.6) )
        
        helpers.setInv()
        slots = []
        for i in range(28):
            if helpers.inv[i]['name'] in itemClearList:
                slots.append(i)
        helpers.dropSlots(slots)
    
    # 2. Travel to forest south of GE
    ###
    ### setRun may be malfunctioning
    ###
    ### start location may be changed
    ###
    if travel:
        if not travelTutExitToGEForest():
            logging.info('Travel TutExit to GEForest failed')
            return False
    
    # 3. Loop to cut logs, sell, and buy supplies:
    if not buySupplies:
        return True
    
    needSupplies = list.copy(supplies)
    while True:
        # a. Chop a full inventory of logs.
        logging.info('Chopping an inventory of logs')
        woodcutter(
            options={'treetype': 'Normal'},
            clientName=clientName,
            endOptions={'condition': 'full'}
            )

        # b. Run to GE
        logging.info('Running to GE')
        helpers.setRun('on')
        while True:
            if (helpers.clickMapImage(
                    'images\\start_comprefGEentrance1.png',
                    timeLimit=15
                    ) or
                helpers.clickMapImage(
                    'images\\start_comprefGEentrance2.png',
                    timeLimit=15
                    ) ):
                time.sleep( random.uniform(8.5, 8.6) )
                break
            helpers.clickMapDirection('n', 0.5)
            time.sleep( random.uniform(5.5, 5.6) )
        logging.info('At GE entrance')
        helpers.clickMapDirection('n')
        time.sleep( random.uniform(9.5, 9.6) )
        logging.info('At GE booth')

        # b2. Sell all logs
        logsSlot = helpers.searchInv('Logs')
        if logsSlot < 0:
            logging.info('Failed to find Logs to sell in inventory')
        else:
            logging.info('Selling logs')
            if not helpers.openGEInterface():
                ### Possible addition:
                ### Do something here to try to return to GE booth
                ### If it still doesn't work, exit function
                return False
            time.sleep( random.uniform(10, 10.1) )
            helpers.sellAndCollect(logsSlot)
            time.sleep( random.uniform(0.2, 0.25) )
            helpers.clickButton('images\\closeviewbutton.png')
            time.sleep( random.uniform(1.5, 1.6) )
        
        # c. If you can afford it, buy supplies.
        coins = helpers.getInvCoins()
        logging.info('Coins: ' + str(coins['amount']))
        logging.info('Need supplies: ')
        logging.info(needSupplies)

        buySupplies = False
        if len(needSupplies) > 0:
            for i in range(len(needSupplies)):
                item = needSupplies[i]
                if coins['amount'] > item['quantity']*item['price']:
                    buySupplies = True
                    break
        if buySupplies:
            # Buy what items you can afford
            boughtItem = True
            while len(needSupplies) > 0 and boughtItem:
                boughtItem = False
                for i in range(len(needSupplies)):
                    item = needSupplies[i]
                    if coins['amount'] > item['quantity']*item['price']:
                        logging.info('Buying ' + item['item'])
                        # Open GE interface
                        if not helpers.openGEInterface():
                            ### Do something here to try to return to GE booth
                            ### If it still doesn't work, exit function
                            return False
                        if not helpers.buyAndCollect(item['item'],
                                item['quantity'], item['price']):
                            continue
                        del needSupplies[i]
                        boughtItem = True
                        time.sleep( random.uniform(1, 1.2) )
                        # Close GE interface
                        helpers.clickButton('images\\closeviewbutton.png')
                        time.sleep( random.uniform(1.5, 1.6) )
                        # Update coins data
                        coins = helpers.getInvCoins()
                        logging.info('Remaining coins: '+str(coins['amount']))
                        break
            
                        
        # d. Return if all supplies are purchased.
        if len(needSupplies) < 1:
            logging.info('Purchased all supplies: ')
            logging.info(supplies)
            return True
        
        logging.info('Running to forest')
        helpers.clickMapDirection('s')
        time.sleep( random.uniform(7, 7.1) )
        helpers.clickMapDirection('sw')
        time.sleep( random.uniform(7, 7.1) )
        if not helpers.searchMapImage('images\\start_comprefGEcorner.png'):
            logging.info('Failed to navigate to forest south of GE')
            return False
        logging.info('Arrived at forest south of GE')
        helpers.setRun('off')
    


"""
Test script
"""
"""
# Get account with specific email
email = 'fumbling47Kiara@mail.com'
account = None
for acc in accounts:
    if acc['credentials'][0] == email:
        account = acc
        break
if account:
    creds = account['credentials']
else:
    print('Failed to find an account with \'done tutorial\' status')

# Login and run startAccount
clientName = 'Old School RuneScape'
worlds = helpers.f2pWorlds
world = worlds[ random.randint(1, len(worlds)-1) ] #any world except 1
helpers.focusClient(clientName)
helpers.login(creds[0], creds[1], world, tutorial=False)
startAccount(clientName,
             supplies=[
                 {'item': 'Rune axe', 'quantity': 1, 'price': 10103}
                ]
            )
"""





    
