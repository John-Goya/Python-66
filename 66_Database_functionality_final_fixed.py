#   John Goya
#
#   For Python Drill #66 - Database Functionality for File Transfer with Python 3.4 & idle.
#   Final initial database issue fixed.

import os
import time
import shutil
import datetime
import sqlite3
import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory

#create root window
root = Tk()

#title for root window
root.title('Backup new files')

#create frames
#top frame
topFrame = Frame(root, width=300, height=50)
topFrame.pack_propagate(0)
topFrame.pack()

#bottom frame
bottomFrame = Frame(root, width=300, height=100)
bottomFrame.pack_propagate(0)
bottomFrame.pack(side=BOTTOM)
bottomFrame.pack(side=BOTTOM)

#variables
src=StringVar()
dst=StringVar()
#backup=StringVar()
lastTime=StringVar()

#database
conn = sqlite3.connect('timestamp.db')
c = conn.cursor()

#timestamp
backuptime = datetime.datetime.now()
#backup.set(backuptime)

#function for source folder button press
def src_callback():
    dir_src = askdirectory()
    src.set(dir_src)
    #return dir_src   
    print ("source backup directory -", dir_src)
    
#function for destination folder button press
def dest_callback():   
    dir_dst = askdirectory()
    dst.set(dir_dst)
    #return dir_dst
    print ("destination backup directory -", dir_dst)

#transfer files - by comparing current time & file modified time     
def fileTransfer(): 
    srcS=src.get()
    dstD=dst.get()
    for fname in os.listdir(srcS):
        path = os.path.join(srcS, fname)
        st = os.stat(path)    
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        oneDay = backuptime - datetime.timedelta(hours = 24)
        if mtime >oneDay:
            shutil.copy(path, dstD)
            print (fname)
            print (mtime)
            timestamp_entry()
'''
#create SQLite table
def create_table():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS backUpTimeStamp(timestamp INTEGER)')
    c.close()
'''

#timestamp entry for table
def timestamp_entry():  
    c.execute('INSERT INTO backUpTimeStamp (timestamp) VALUES (?)',
              (backuptime,))
    conn.commit()
    c.close
#function for backup button press
def transferTimeStamp():
    #create_table()
    getBackupTime()
    fileTransfer()
   
#retrieve last backup time/date & output to UI
def getBackupTime():
    c.execute('SELECT * FROM backUpTimeStamp ORDER BY timestamp DESC Limit 1')
    #l_time = c.fetchone()
    print(l_time)
    #lastTime.set(l_time)

#create the SQLite timestamp table
c.execute('CREATE TABLE IF NOT EXISTS backUpTimeStamp(timestamp INTEGER)')

#retrieve last timestamp & assign variable to display on UI
c.execute('SELECT * FROM backUpTimeStamp ORDER BY timestamp DESC Limit 1')
l_time = c.fetchone()
#print(l_time)
lastTime.set(l_time)


#size window
sourceButton = Button(topFrame, wraplength=120, text='Select folder to backup:',
    command= src_callback, width=15).pack(padx=15, pady=5, side=LEFT)
#sourcePath = Entry(bottomFrame,text=src).pack()
destinationButton = Button(topFrame, wraplength=120, text='Select backup destination folder:',
    command=dest_callback, width=15).pack(padx=15, pady=5, side=RIGHT)
#destPath = Entry(bottomFrame, text=dst).pack()
executeButton = Button(bottomFrame, wraplength=120, text='Check files and backup!',
    command=transferTimeStamp, width=15, fg='green').pack(pady=5)
#timestamp1 = Label(bottomFrame,wraplength=120, textvariable=backup).pack()
timestamp = Label(bottomFrame, textvariable=lastTime).pack()

#main event loop - to keep buttons on screen
root.mainloop()
