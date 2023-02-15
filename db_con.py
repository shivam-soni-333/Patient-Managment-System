import sqlite3
from tkinter import messagebox
import os

con=None
cur=None
try:
    if os.path.isfile('receipt_system.db'):
        con = sqlite3.connect('receipt_system.db')
    else:
        messagebox.showerror("Error","can not find database file")
    cur = con.cursor()        
except:
    messagebox.showerror("Error","Unable to connect with database")

