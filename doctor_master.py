from multiprocessing import parent_process
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_con import cur,con
from tkinter.ttk import *
class doctor_master(Toplevel):
    des  = 0 #des used for make sure that user not selected any of treeview entry (when pree entry on last entry it goes to add function so that can be stop using des var (when user is on editing mode ))
    def __init__(self,master=None):
        super().__init__(master=master)
        self.doctor_master_root = self
        self.doctor_master_root.title("Doctor Master")
        self.doctor_master_root.resizable(False,False)

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.doctor_master_root.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        window_height = 550
        window_width = 300
    
        screen_width = self.doctor_master_root.winfo_screenwidth()
        screen_height = self.doctor_master_root.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.doctor_master_root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.doctor_master_root.focus_force()
        self.doctor_master_root.update()        




        #doc id label  
        self.doc_id_label = Label(self.doctor_master_root,text="")
        # doc_id_label.config(text="1")
        self.doc_id_label.place(x=0,y=40)
        
        
        #name lable and entry 
        name_lbl = Label(self.doctor_master_root,text="Name :- ")
        name_lbl.grid(row=1,column=5)

        self.name_var = StringVar()
        self.name_entry = Entry(self.doctor_master_root,width=30,textvariable=self.name_var)
        self.name_entry.focus()
        self.name_entry.grid(row=1,column=7)
        self.name_entry.bind("<Return>",lambda funct1:self.add_to_db())
        
        #treeview
        col = ('DocId','Doctor Name')
        self.tree = ttk.Treeview(self.doctor_master_root,column=col,show='headings',height=17)

        self.tree.heading('DocId',text='DocId')
        self.tree.heading('Doctor Name',text="Doctor Name")
        
        self.tree.column("0",width="30")
        self.tree.column("0",width="50")
        
        self.tree.place(x=10,y=80)
       
        self.tree.bind("<<TreeviewSelect>>",self.get_selection)

        scrollbar = ttk.Scrollbar(self.doctor_master_root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=290,y=78,height=390)

      
        self.display_data()
        self.next_doc_id()
        #button
        self.add = Button(self.doctor_master_root,text="Add",width=15,command=self.add_to_db)
        self.add.place(x=90,y=35)
        
        self.edit = Button(self.doctor_master_root,text="Edit",width=8,command=self.update_record)
        self.edit.place(x=20,y=500)
        self.edit['state']='disabled'

        self.delete = Button(self.doctor_master_root,text="Delete",width=8,command=self.delete_record)
        self.delete.place(x=110,y=500)
        self.delete['state']='disabled'

        exit_btn = Button(self.doctor_master_root,text="Exit",width=8,command=lambda:self.doctor_master_root.destroy())
        exit_btn.place(x=200,y=500)
        
        self.clear = Button(self.doctor_master_root,text="Clear Selection",width=20,command=self.clear_selection)
        self.clear.place(x=90,y=35)
        self.clear.place_forget()


        #shortcut label 
        Label(self.doctor_master_root,text="ctrl+e").place(x=40,y=535)
        Label(self.doctor_master_root,text="ctrl+d").place(x=130,y=535)
        Label(self.doctor_master_root,text="esc").place(x=230,y=535)

        
        self.doctor_master_root.bind("<Control-d>",self.ctrl_d)
        self.doctor_master_root.bind("<Control-e>",self.ctrl_e)
        self.doctor_master_root.bind("<Escape>",lambda e:self.doctor_master_root.destroy())
      

        self.doctor_master_root.mainloop()
    
    
  


    def add_to_db(self): 
        if self.des == 0:
            self.add['state']='disabled'
            nm = self.name_var.get()
            nm  = nm.replace("'","").replace('"',"").strip()
            if nm == "":
                messagebox.showerror(" Invalid input "," Empty Field",parent=self.doctor_master_root)
                self.add['state']='normal'
                return
            try:
                cur.execute(f"insert into doctor(name) values('{nm}')")
                con.commit()
                self.display_data()
                self.name_var.set("")
                messagebox.showinfo("Success!!!","Doctor Added Successfully",parent=self.doctor_master_root)
                self.add['state']='normal'
            except Exception as e:
                print(e)
                self.add['state']='normal'
                messagebox.showerror("Error while inserting doctor","there is an error while inserting doctor to database")

    def display_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cur.execute("select * from doctor")
        for i in cur.fetchall():
            self.tree.insert('','end',text="",values=i)
        self.next_doc_id()        

    def get_selection(self,e):
        
        self.edit['state']='normal'
        self.delete['state']='normal'
        values = []
        i = ""
        for item in self.tree.selection():
            i = item
            values = self.tree.item(item,'values')
        
        if len(values)>0:    
            try:
                self.name_var.set(str(values[1]))
                
                self.doc_id_label['text']="Doc Id :- "+str(values[0])
                pos = len(self.name_var.get())
                self.name_entry.icursor(pos)
                self.clear.place(x=90,y=35)
                self.des=1
            except Exception as e:
                print(e)
                self.next_doc_id()
                messagebox.showerror("error","Can not able to select doctor from treeview ...",parent=self.doctor_master_root)
            
    def clear_selection(self):
       
        self.next_doc_id()
        self.des=0
        self.name_var.set("")
        self.name_entry.focus()
        for i in self.tree.selection():
            self.tree.selection_remove(i)
        
        self.doctor_master_root.update()
        self.edit['state'] = 'disabled'
        self.delete['state'] = 'disabled'
    
        self.clear.place_forget()
        

    def nothing(self,e):
       pass
    
        
        

    def next_doc_id(self):
        try:
            cur.execute("select seq from sqlite_sequence where name='doctor'")
            out = cur.fetchone()
            if out != None:
                self.doc_id_label['text'] ="Doc Id :- "+ str(int(out[0])+1)
            else:
                raise Exception
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Unable to fetch next doctor id",parent=self.doctor_master_root)
    
    def update_record(self):
        res = messagebox.askquestion("?","Are you Sure you want to update record ? ",parent=self.doctor_master_root)
        if res == "yes":
            self.edit['state']='disabled'
            values = []
            i = ""
            for item in self.tree.selection():
                i = item
                values = self.tree.item(item,'values')
            name = self.name_var.get().replace("'","").replace('"',"").strip()
          
            if name =="":
                self.edit['state']='normal'
                messagebox.showerror("Invalid Input "," Empty Fields ",parent=self.doctor_master_root)
                self.clear_selection()
                return

            if len(values)>0 and name != "" and len(name) > 0:    
                try:
                    cur.execute(f"update doctor set name='{name}' where id={values[0]} ")
                    con.commit()
                    messagebox.showinfo("Success","Name Updated Succesfully",parent=self.doctor_master_root)
                    self.edit['state']='normal'
                    self.clear_selection()
                    self.display_data()
                except:
                    messagebox.showerror("Error","Error while Updating Record",parent=self.doctor_master_root)
                    self.edit['state']='normal'

    def delete_record(self):
        res = messagebox.askquestion("?","Are you sure you want to delete record?",parent=self.doctor_master_root)
        if res =="yes":
            self.delete['state']='disabled'
            try:
                values = []
                for item in self.tree.selection():
                    values = self.tree.item(item,'values')
                if(len(values)>0):
                    cur.execute(f"delete from doctor where id={values[0]}")
                    con.commit()
                    self.clear_selection()
                    self.display_data()
                    messagebox.showinfo("Success!!!","Record Deleted Succesfully",parent=self.doctor_master_root)
               
            except:
                self.delete['state']='normal'
                messagebox.showerror("Error","Can not delete record",parent=self.doctor_master_root)
        
    def ctrl_d(self,e):
        if self.des==1:
            self.delete_record()
        else:
            messagebox.showerror("Unable to delete doctor","Please select doctor that you want to delete",parent=self.doctor_master_root)
        
    def ctrl_e(self,e):
       
        if self.des==1:
            self.update_record()
        else:
            messagebox.showerror("unable to edit doctor","Please select doctor that you want to edit",parent=self.doctor_master_root)
        
# test = doctor_master()
