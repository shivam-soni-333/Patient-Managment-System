# new doctor contain main frame of software

from operator import imod
from tkinter import *
from case_entry import case_entry
from charge_master import charge_master
from doctor_master import doctor_master
from department_master import department_master
from charge_master import charge_master
from tkinter import messagebox
from tkinter.ttk import *
from case_entry import case_entry
from year_master import year_master
from all_receipt import all_receipt
from PIL import Image,ImageTk
from change_password import change_password
from change_path import change_path
from collection_summary import collection_summary
from collection_summary_receipt_wise import receipt_wise
from backup import backup
from db_con import con,cur
class main_frame():
    def __init__(self):
       
        self.main_frame = Tk()
        
        

        w, h = self.main_frame.winfo_screenwidth(), self.main_frame.winfo_screenheight()
        self.main_frame.geometry("%dx%d+0+0" % (w, h))
        self.main_frame.focus_force()
        self.main_frame.title("Receipt System")
        self.main_frame.update()

        try:
            self.main_frame.tk.call('source', r'Forest-ttk-theme-master\forest-light.tcl')
        except:
            messagebox.showerror("Error","Unable to load theme")

        Style().theme_use('forest-light')

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main_frame.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        try:
            canvas = Canvas(self.main_frame,width=w,height=h)
            canvas.pack()
            canvas.configure(background='white')

            try:
                file=Image.open("./images/l.png")
            except:
                messagebox.showerror("Error","Can not find image folder",parent=self.main)
                return
            pilImage = file
            imgWidth, imgHeight = pilImage.size
    
            ratio = min(w/imgWidth, h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)   
            image = ImageTk.PhotoImage(pilImage)
            
            imagesprite = canvas.create_image(w/2,h/2,image=image)
        except:
            messagebox.showerror('!',"can not set background images",parent=self.main)

     

        menubar = Menu(self.main_frame)

        master = Menu(menubar,tearoff=0) #master is first menu
        print(self.main_frame)
        master.add_command(label="Doctor Master",command=lambda :doctor_master(self.main_frame))
        master.add_command(label="Department Master",command=lambda :department_master(self.main_frame))
        master.add_command(label="Fee/Charge Master",command=lambda: charge_master(self.main_frame))
        master.add_command(label="Year Master",command=lambda:year_master(self.main_frame))
        menubar.add_cascade(label="Master",menu=master)

        #transaction menu  
        transaction = Menu(menubar,tearoff=0)
        transaction.add_command(label="Case Entry |   F1",command=lambda : case_entry(self.main_frame))
        transaction.add_command(label="All Receipt",command=lambda : all_receipt(self.main_frame))
        menubar.add_cascade(label="Transaction",menu=transaction)


        #Report
        report = Menu(menubar,tearoff=0)
        report.add_command(label="Collection summary department wise",command=lambda:collection_summary(self.main_frame))
        report.add_command(label="Collection summary receipt wise",command=lambda:receipt_wise(self.main_frame))
        menubar.add_cascade(label="Reports",menu=report)

        #backup
        backup_var = Menu(menubar,tearoff=0)
        backup_var.add_command(label="Backup",command=lambda:backup(self.main_frame))
        menubar.add_cascade(label="Backup",menu=backup_var)

        #settings
        settings = Menu(menubar,tearoff=0)
        settings.add_command(label="Change Password",command = lambda:change_password(self.main_frame))
        settings.add_command(label="Change path for save receipt",command=lambda:change_path(self.main_frame))        
        menubar.add_cascade(label="Settings",menu=settings)
        
        self.main_frame.config(menu=menubar)

        # self.main_frame.bind('<Alt-F4>',self.alt_f4)
        self.main_frame.protocol("WM_DELETE_WINDOW", self.alt_f4)
        self.main_frame.bind("<F1>",lambda e:case_entry(self.main_frame))
        self.main_frame.bind("<Escape>",self.alt_f4)

        cur.execute("select * from year ")
        out  = cur.fetchone()
        if out != None:
            pass
        else:
            messagebox.showerror("No Year Found","Please Entrt Year First",parent=self.main_frame)
            year_master(self.main_frame)

        cur.execute("select * from path_for_saving_receipt")
        out = cur.fetchone()
        if out != None:
            pass
        else:
            messagebox.showerror("No Path found for saving receipt","Please select path for saving receipt",parent=self.main_frame)
            change_path(self.main_frame)
        
        self.main_frame.mainloop()
    
    def alt_f4(self,e=None):
        res = messagebox.askquestion("Quit?","Do you want to Quit?")
        if res == "yes":
            self.main_frame.destroy()
            
    

      