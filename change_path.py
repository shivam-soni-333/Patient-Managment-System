from email import message
from tkinter import *
from db_con import con,cur
from tkinter import filedialog
from tkinter import messagebox
import os 
import os.path
from tkinter.ttk import *
class change_path(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)

        self.main = self
        self.main.resizable(False,False)
        
        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        
        window_height = 300
        window_width = 500
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.main.focus_force()
        self.main.update()
        Label(self.main,text="Current Path For Saving Receipt :- ").place(x=5,y=0)
        self.current_path = Label(self.main,text="")
        self.current_path.place(x=5,y=20)
        
        self.current_path_f()

        Label(self.main,text="Change Path :- ").place(x=10,y=70)

        self.open_btn = Button(self.main,text="Select Path ",width=20,command=self.open)
        self.open_btn.place(x=100,y=70)
        
        self.selected_path = Label(self.main,text="")
        self.selected_path.place(x=10,y=100)

        self.change_btn = Button(self.main,text="Change",width=20,command=self.save_path)
        self.change_btn.place(x=100,y=130)
        self.change_btn['state']  = 'disable'
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        
        # Label(self.main,text="This path will be used for save receipt").place(x=10,y=30)

    def current_path_f(self):
        try:
            cur.execute("select *  from path_for_saving_receipt")
            out = cur.fetchone()
            print(out)
            if out != None:
                self.current_path['text'] =  out[1] 
            else:
                messagebox.showerror("Can not find path","Please enter path for saving receipt",parent=self.main)
        except Exception as e:
            messagebox.showerror("Can not find path","Please enter path for saving receipt",parent=self.main)
            
    
    def open(self):
        self.path = filedialog.askdirectory(parent=self.main)
        self.selected_path['text'] = "You selected :- "+ str(self.path) 
        self.change_btn['state'] = 'normal'
        self.open_btn['state'] = 'disable'
    
    def save_path(self):
        res = messagebox.askquestion("?",f"Do you really want to set this {self.path} path for saving receipt ?",parent=self.main)
        if res == "yes":
            temp = self.path + "/saved_receipt"
            print(temp)
            if not os.path.isdir(temp):
                try:
                    os.mkdir(temp)
                except:
                    messagebox.showerror('Error',"error while creating directory saved_receipt ",parent=self.main)
                    self.selected_path['text'] = ""
                    self.current_path_f()
                    self.change_btn['state'] = "disable"
                    self.open_btn['state'] = 'normal'
                    return
                
            cur.execute("select * from path_for_saving_receipt")
            out = cur.fetchone()
            if out != None:
                try:
                    cur.execute(f"update path_for_saving_receipt set folderpath = '{temp}' ")
                    con.commit()
                    messagebox.showinfo("!","Path Changed Succesfully",parent=self.main)
                except:
                    messagebox.showerror("!","Error while updating path",parent=self.main)
                      
            else:
                try:
                    cur.execute(f"insert into path_for_saving_receipt(folderpath) values('{temp}')")
                    con.commit()
                    messagebox.showinfo("!","Path Changed Succesfully",parent=self.main)
            
                except:
                    messagebox.showerror("!","Error while inserting path",parent=self.main)
                   
            
            self.selected_path['text'] = ""
            self.current_path_f()
            self.change_btn['state'] = "disable"
            self.open_btn['state'] = 'normal'
                
        

