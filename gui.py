#! python3

"""
GUI for user to input credentials and select
script options.
"""

import logging
import tkinter
from tkinter import ttk
from tkinter import filedialog

logging.basicConfig(level=logging.INFO)

##
## Warning: loginGui is incomplete. Saving info is not implemented,
## and the function has not been tested much. The current plan is to
## leave startup/login to the user. This function is preserved in
## case I decide, later, to handle that in the program.
##
def loginGui():
    # Create root window and main content frame
    root = tkinter.Tk()
    root.title('Start client and login')
    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky='nwes')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # Create and arrange widgets/labels
    client = tkinter.StringVar()
    clientWdg = ttk.Combobox(mainframe, textvariable=client)
    clientWdg.grid(column=2, row=1, sticky='we')
    clientWdg['values'] = ('RuneLite', 'OSBuddy', 'Konduit', 'Official')
    ttk.Label(mainframe, text='Client:').grid(column=1, row=1, sticky='e')

    clientPath = tkinter.StringVar()
    def clientPathWdgClick():
        global clientPath
        selectedPath = filedialog.askopenfilename(
            initialdir = "C:/",
            title = "Select client program",
            filetypes = (('executable', '*.exe'), ('all files', '*.*'))
            )
        clientPath.set(selectedPath)
    clientPathWdg = ttk.Button(mainframe, text='Select file', command=clientPathWdgClick)
    clientPathWdg.grid(column=2, row=2, sticky='we')
    ttk.Label(mainframe, text='Client path:').grid(column=1, row=2, sticky='e')
    ttk.Label(mainframe, textvariable=clientPath).grid(column=3, row=2, sticky='w')

    username = tkinter.StringVar()
    usernameWdg = ttk.Entry(mainframe, textvariable=username)
    usernameWdg.grid(column=2, row=3, sticky='we')
    ttk.Label(mainframe, text='Username:').grid(column=1, row=3, sticky='e')

    password = tkinter.StringVar()
    passwordWdg = ttk.Entry(mainframe, textvariable=password, show='*')
    passwordWdg.grid(column=2, row=4, sticky='we')
    ttk.Label(mainframe, text='Password:').grid(column=1, row=4, sticky='e')

    saveInfo = tkinter.IntVar()
    saveInfo.set(1)
    saveInfoWdg = ttk.Checkbutton(mainframe, variable=saveInfo, text='Remember info')
    saveInfoWdg.grid(column=2, row=5)

    def loginWdgClick():
        if saveInfo.get():
            logging.info('Save info')
        if not helpers.startClient(client.get(), clientPath.get()):
            print('Could not start client. Exiting')
            root.destroy()
            sys.exit(0)
        helpers.login(username.get(), password.get(), 393)
        
        root.destroy()
    loginWdg = ttk.Button(mainframe, text='Login', command=loginWdgClick)
    loginWdg.grid(column=2, row=6, sticky='wes')

    def cancelWdgClick():
        logging.info('Clicked cancel')
        root.destroy()
    loginWdg = ttk.Button(mainframe, text='Cancel', command=cancelWdgClick)
    loginWdg.grid(column=3, row=6, sticky='es')

    # Launch window
    root.mainloop()


# Display a GUI allowing user to select options and start script.
# Returns these tkinter vars you can use to get user's chosen options:
#   treetype, bank, start
def woodcutterStartGui():
    # Create root window and main content frame
    root = tkinter.Tk()
    root.title('Start options')
    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky='nwes')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # Create and arrange widgets/labels
    treetype = tkinter.StringVar()
    treetype.set('Normal')
    normal = ttk.Radiobutton(
        mainframe,text='Normal',variable=treetype,value='Normal'
        )
    oak = ttk.Radiobutton(
        mainframe,text='Oak',variable=treetype,value='Oak'
        )
    willow = ttk.Radiobutton(
        mainframe,text='Willow',variable=treetype,value='Willow'
        )
    yew = ttk.Radiobutton(
        mainframe,text='Yew',variable=treetype,value='Yew'
        )
    ttk.Label(mainframe, text='Select tree type:').grid(column=1, row=1, sticky='w')
    normal.grid(column=1, row=2, sticky='w')
    oak.grid(column=1, row=3, sticky='w')
    willow.grid(column=1, row=4, sticky='w')
    yew.grid(column=1, row=5, sticky='w')

    bank = tkinter.IntVar()
    bankWdg = ttk.Checkbutton(
        mainframe, variable=bank, text='Bank logs'
        )
    bankWdg.grid(column=2, row=3, sticky='e')

    start = tkinter.StringVar()
    def startWdgClick():
        start.set('Start')
        root.destroy()
    startWdg = ttk.Button(mainframe, text='Start', command=startWdgClick)
    startWdg.grid(column=1, row=5, sticky='wes')

    def cancelWdgClick():
        start.set('Cancel')
        root.destroy()
    cancelWdg = ttk.Button(mainframe, text='Cancel', command=cancelWdgClick)
    cancelWdg.grid(column=2, row=5, sticky='es')

    # Launch window and return vars
    root.mainloop()
    return {'treetype': treetype, 'bank': bank, 'start': start}








        
    


