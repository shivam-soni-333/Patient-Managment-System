from tkinter import *
from tkinter import messagebox
from db_con import cur 
from tkinter.ttk import * 
from new_doctor import main_frame



class login:
    def __init__(self,parent_window):
        self.main   = parent_window
        self.main.title("Login")
        self.main.resizable(False,False)

        

        try:
            self.main.tk.call('source', r'Forest-ttk-theme-master\forest-light.tcl')
        except:
            messagebox.showerror("Error","Unable to load theme")

        Style().theme_use('forest-light')


        window_height = 150
        window_width = 300
    
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        main.focus_force()

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Could not find logo file")
         
        #label  for username
        Label(main,text="Username :- ").grid(row = 0,column = 0)
        
        #entry for username
        self.username_var = StringVar()
        # self.username_var.set("admin")
        self.username_entry = Entry(main,width=25,textvariable = self.username_var)
        self.username_entry.focus_set()
        self.username_entry.grid(row=0,column=1)
        self.username_entry.bind("<Return>",lambda funct1:self.password_entry.focus())

        #password label
        Label(main,text="Password :- ").grid(row=1,column=0,pady=15)

        #password entry
        self.password_var = StringVar()
        # self.password_var.set("admin")
        self.password_entry = Entry(main,show='*',width=25,textvariable=self.password_var)
        self.password_entry.grid(row=1,column=1,pady=15)
        self.password_entry.bind("<Return>",lambda funct1:self.login())

        #button 
        

        self.login_btn = Button(main,text="Login",command=self.login)
        self.login_btn.grid(row=2,column=1)
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if(username !="" and password !=""):
            
            cur.execute(f"select * from user where username='{username}' and password = '{password}' ")

            if(cur.fetchone() != None):
                # messagebox.showinfo("success","login success")
                main.destroy()
                main_frame()

            else:
                messagebox.showerror("Error","Invalid Username/Password")
        else:
            messagebox.showerror("Empty Fields","Invalid Input")

main=Tk()
login_obj = login(main)
main.mainloop()
