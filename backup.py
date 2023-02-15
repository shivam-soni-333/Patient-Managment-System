from email import message_from_bytes
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import filedialog
import sqlite3
import io
import datetime

class backup(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.main = self

      

        self.main.title("Backup ")
        self.main.resizable(False,False)

        window_height = 300
        window_width = 500
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()-30 # - 30 for proper setting up screen on main window

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
         
        self.main.focus_force()
        self.main.update()


        
        self.open_btn = Button(self.main,text="Open ",width=20,command=self.open)
        self.open_btn.place(x=150,y=10)

        Label(self.main,text="Select Path for backup").place(x=10,y=10)


              
        self.selected_path = Label(self.main,text="")
        self.selected_path.place(x=10,y=60)

        self.change_btn = Button(self.main,text="Backup",width=20,command=self.save_path)
        self.change_btn.place(x=100,y=100)
        self.change_btn['state']  = 'disable'
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        


 
    def open(self):
        self.path = filedialog.askdirectory(parent=self.main)
        self.selected_path['text'] = "You selected :- "+ str(self.path) 
        self.change_btn['state'] = 'normal'
        self.open_btn['state'] = 'disable'
    
    def save_path(self):
        try:
            conn = sqlite3.connect('receipt_system.db')
        except:
            messagebox.showerror("can not connect to database","Unable to connect database",parent=self.main)
            return
     
        creation_dt = str(datetime.datetime.today()).replace("/","_").replace(":","_").replace(" ","_")

        with io.open(f'{self.path}/backup_receipt_system_{creation_dt}.sql', 'w') as p:
            # iterdump() function
            for line in conn.iterdump():
                p.write('%s\n' % line)
        conn.close()
        messagebox.showinfo("Success","Backup Succesfully",parent=self.main)
        self.selected_path['text'] = ""
        self.change_btn['state']='disable'
        self.open_btn['state'] = 'normal'
