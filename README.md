# osrs

!['osrs_screenshot'](docs/osrsbot.png)

## Botting programs for Old School RuneScape

This collection of scripts will do some basic tasks in the video game Old School RuneScape.
They interact with the official game client by reading the screen and simulating keyboard/mouse events.

Main packages:
- PIL to process screenshots
- PyAutoGUI to simulate keyboard/mouse events
- tkinter to setup and kickoff scripts in a GUI

### Warning

***DO NOT USE THESE SCRIPTS ON AN ACCOUNT YOU'RE NOT WILLING TO LOSE!***
Bot detection WILL detect and ban your account.
Small tweaks to the game or client can cause these scripts to malfunction.
Finally, these scripts haven't been maintained since 2018, so there are probably some major bugs.

### Run instructions

You will need [Python 3](https://www.python.org/downloads/) with [pip](https://pip.pypa.io/en/stable/installing/), and the official [Old School RuneScape client](https://www.runescape.com/oldschool/download).

1. Clone this github repo OR download and unzip this repo
2. Go the downloaded project directory and run: ```pip install -r .\requirements.txt```
3. Run: ```python main.py```
4. Set the script options and then kick it off

### Scripts

1. woodcutter.py
   - Automatically cut and drop normal trees, oaks, and willows; bank some log types

2. tutorial.py
   - Complete Tutorial Island

3. makeAccount.py
   - Register new accounts on the RuneScape website and store the account credentials

4. startAccount.py
   - On a new account (fresh out of Tutorial Island), use woodcutting profits to acquire a list of starting supplies from the Grand Exchange
