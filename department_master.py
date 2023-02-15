from multiprocessing import parent_process
from tkinter import *
from tkinter.ttk import *
from turtle import width
from db_con import cur,con
from tkinter import messagebox
class department_master(Toplevel):
    des = 0 #des used for make sure that user not selected any of treeview entry (when pree entry on last entry it goes to add function so that can be stop using des var (when user is on editing mode ))
    def __init__(self,master=None):
        super().__init__(master=master)
        self.dep_main = self
        
        self.dep_main.title("Department Master")
        self.dep_main.resizable(False,False)


        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.dep_main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        window_height = 600
        window_width = 300
    
        screen_width = self.dep_main.winfo_screenwidth()
        screen_height = self.dep_main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))
        
        self.dep_main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.dep_main.focus_force()
        self.dep_main.update()
        
        Label(self.dep_main,text="Dept Name :- ").grid(row=1,column=0)
        self.dept_name_var = StringVar()
        self.dept_entry = Entry(self.dep_main,width=25,textvariable=self.dept_name_var)
        self.dept_entry.focus()
        self.dept_entry.grid(row=1,column=1)
        
        self.dept_entry.bind("<Return>",lambda funct1:self.add_to_db())
        
     
       
        self.dep_code = Label(self.dep_main,text="")
        self.dep_code.place(x=0,y=40)
        self.next_dep_code()
        col = ('dep_id','dep_name')
        self.tree =  Treeview(self.dep_main,column=col,show='headings',height=17)
        
        self.tree.heading('dep_id',text="DepCode")
        self.tree.heading('dep_name',text="Department Name")
     
        self.tree.column("0",width="50")
        self.tree.column("1",width="200")
       

        self.tree.place(x=5,y=120)
        
        
        scrollbar = Scrollbar(self.dep_main, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=284,y=120,height=400)

      
        self.add  = Button(self.dep_main,text="Add",width=20,command=self.add_to_db)
        self.add.place(x=80,y=70)

        self.clear = Button(self.dep_main,text="Clear Selection",width=20,command=self.clear_selection)
        self.clear.place(x=80,y=70)
        self.clear.place_forget()

        self.edit = Button(self.dep_main,text="Edit",width=10,command=self.update_record)
        self.edit.place(x=10,y=540)
        self.edit['state']='disable'

        #shortcut label 
        Label(self.dep_main,text="ctrl+e").place(x=25,y=578)
        Label(self.dep_main,text="ctrl+d").place(x=125,y=578)
        Label(self.dep_main,text="esc").place(x=240,y=578)

        
        self.delete = Button(self.dep_main,text="Delete",width=10,command=self.delete_record)
        self.delete.place(x=110,y=540)

        self.delete['state']='disable'
        self.exit = Button(self.dep_main,text="Exit",width=10,command=self.dep_main.destroy)
        self.exit.place(x=210,y=540)
        
        self.display_data()

        self.dep_main.bind("<Control-d>",self.ctrl_d)
        self.dep_main.bind("<Control-e>",self.ctrl_e)
        self.dep_main.bind("<Escape>",lambda e:self.dep_main.destroy())
        self.dep_main.bind("<<TreeviewSelect>>",self.get_selection)
        self.dep_main.update()
        self.dep_main.mainloop()
    
    def set_focus(self,widget,widget_var):
        pos = len(widget_var.get())
        widget.focus()
        widget.icursor(pos)

    def display_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cur.execute("select * from department")
        for i in cur.fetchall():
            self.tree.insert('','end',text="",values=i)

    def add_to_db(self):
        if self.des ==0:
            self.add['state']='disable'
            name = str(self.dept_name_var.get()).replace("'","").replace('"',"").strip()
            
            if(name !="" ):
                try:
                    cur.execute(f"insert into department(name) values('{name}')")
                    last_row_id = str(cur.lastrowid)
                    seq_nm = "dept_" + last_row_id
                    cur.execute(f"select id from year where is_current_year=1")
                    out = cur.fetchone()
                    if out != None:
                        cur.execute(f"insert into manage_receipt_no(receipt_no,year,dept_id) values(1,{out[0]},{last_row_id})")
                        con.commit()
                    else:
                        messagebox.showerror("can not find current year id","Please enter year in year master",parent=self.dep_main)
                        self.add['state'] = 'normal'
                        return
                    self.add['state'] = 'normal'
                    self.next_dep_code()
                    messagebox.showinfo("Success!","Department Added Succesfully",parent=self.dep_main)
                    self.display_data()
                    self.dept_name_var.set("")
                    self.dept_entry.focus()
                except Exception as e:
                    print(e)
                    self.add['state']='normal'
                    messagebox.showerror("Error while adding department","Cannot able to add department",parent=self.dep_main)
            else:
                self.add['state']='normal'
                messagebox.showerror("Invalid Input"," Empty Fields! ",parent=self.dep_main)
       

    def next_dep_code(self):
        try:
            cur.execute("select seq from sqlite_sequence where name='department'")
            out = cur.fetchone()
            if out != None:
                self.dep_code['text'] ="Dept. Code :-   "+str(int(out[0])+1)
            else:
                raise Exception
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Unable to fetch next Department Id",parent=self.dep_main)

    def get_selection(self,e):
        self.des = 1
        self.edit['state']='normal'
        self.delete['state']='normal'
        values = []
        i = ""
        for item in self.tree.selection():
            i = item
            values = self.tree.item(item,'values')
       
        if len(values)>0:    
            try:
                self.dep_code['text'] = "Dept. Code :-  "+str(values[0])
                self.dept_name_var.set(str(values[1]))
                self.clear.place(x=80,y=70)
            except Exception as e:
                print(e)
                self.next_dep_code()
                messagebox.showerror("error","Can not able to select doctor from treeview ...",parent=self.dep_main)

  
    def clear_selection(self):

        for i in self.tree.selection():
            self.tree.selection_remove(i)
       
        self.dep_main.update()
        self.edit['state']='disable'
        self.delete['state']='disable'

        self.dept_name_var.set("")
        self.next_dep_code()
        self.des =0
        self.clear.place_forget()
    
    def update_record(self):
        res = messagebox.askquestion("?","Are you sure you want to update department ?",parent=self.dep_main)
        if res =="yes":
            values = []
            i = ""
            for item in self.tree.selection():
                i = item
                values = self.tree.item(item,'values')
            
            name = str(self.dept_name_var.get()).replace("'","").replace('"','').strip()
           
            if(name !=""):
                try:
                    cur.execute(f"Update department set name='{name}'  where id={values[0]}")
                    con.commit()
                    messagebox.showinfo("Success","Department Updated Succesfully",parent=self.dep_main)
                    self.display_data()
                    self.clear_selection()
                except:
                    messagebox.showerror("error","Can not able to update department",parent=self.dep_main)
            else:
                messagebox.showerror("Invalid Input"," Empty Fields",parent=self.dep_main)
       

    

    def delete_record(self):
        res = messagebox.askquestion("?","Are you sure you want to delete this department ?",parent=self.dep_main)
        if res =="yes":
            self.delete['state']='disable'
            val = []
            
            for item in self.tree.selection():
                val = self.tree.item(item,'values')
            if len(val)>0:
                try:
                    cur.execute(f"delete from department where id = {val[0]}")
                    con.commit()
                    messagebox.showinfo("success!!!","Department Deleted successfully",parent=self.dep_main)
                    self.display_data()
                    self.clear_selection()
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error","can not able to delete department",parent=self.dep_main)
            else:
                messagebox.showerror("Oh","You Forget to select department !")

    def ctrl_d(self,e):
    
        if self.des==1:
            self.delete_record()
        else:
            messagebox.showerror("Unable to delete department","Please select record that you want to delete",parent=self.dep_main)
        
    def ctrl_e(self,e):
        if self.des==1:
            self.update_record()
        else:
            messagebox.showerror("unable to edit department","Please select record that you want to edit",parent=self.dep_main)
        