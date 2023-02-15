from cgitb import text
from tkinter import *
from tkinter import messagebox 
from tkinter.ttk import *
from db_con import con,cur

class change_password(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)

        self.main = self
        self.main.title("Change Password")

        self.main.resizable(False,False)


        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        window_height = 200
        window_width = 300
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.main.focus_force()
        self.main.update()

        Label(self.main,text="Username").place(x=10,y=10)

        self.username_var = StringVar()
        self.username = Entry(self.main,width=20,textvariable=self.username_var)
        self.username.place(x=130,y=10)    
        self.username.focus()   
        self.username.bind("<Return>",lambda e:self.password.focus())

        Label(self.main,text="new password").place(x=10,y=60)
        self.password_var = StringVar()
        self.password = Entry(self.main,show="*",width=20,textvariable=self.password_var)
        self.password.place(x=130,y=55,height=28)
        self.password.bind("<Return>",lambda f:self.password_2.focus())

        Label(self.main,text="Confirm password").place(x=10,y=105)
        self.password_2_var = StringVar()
        self.password_2 = Entry(self.main,show="*",width=20,textvariable=self.password_2_var)
        self.password_2.place(x=130,y=100,height=28)
        self.password_2.bind("<Return>",lambda e:self.change_pass())

        self.change = Button(self.main, text="Change Password",width=20,command=self.change_pass)
        self.change.place(x=80,y=150)
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        

    def change_pass(self):   
        username=str(self.username_var.get()).replace("'","").replace('"','').strip()
        pass1 = str(self.password_var.get()).replace("'","").replace('"','').strip()
        pass2 = str(self.password_2_var.get()).replace("'","").replace('"','').strip()

        if username !="" and pass1 !="" and pass2!="":
        
            if pass1 == pass2:
                try:
                    cur.execute(f"update user set username = '{username}' , password = '{pass1}'")
                    con.commit()
                except:
                    pass
                messagebox.showinfo("!","Password changed Succesfully",parent=self.main)
                self.username_var.set("")
                self.password_var.set("")
                self.password_2_var.set("")
                self.username.focus()
            
            else:
                messagebox.showwarning("!","Password and confirm password not matched",parent=self.main)
                return