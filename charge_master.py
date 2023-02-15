from ast import excepthandler
import imp
from io import StringIO
from multiprocessing import parent_process
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from db_con import con,cur

from department_master import department_master

class charge_master(Toplevel):
    des = 0  # des = 0 add mode else des == 1 then it is in editing mode
    edit_id  = 0 #this is for storing charge id which user want to edit 
    dept_id_lst = []
    def __init__(self,master=None):
        super().__init__(master=master)
        self.charge_master_main = self
        
        self.charge_master_main.title("Fee / Charge Master")
        self.charge_master_main.resizable(False,False)

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.charge_master_main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        window_height = 600
        window_width = 325
    
        screen_width = self.charge_master_main.winfo_screenwidth()
        screen_height = self.charge_master_main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.charge_master_main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.charge_master_main.focus_force()
        self.charge_master_main.update()

        #charge name
        Label(self.charge_master_main,text="Fee Name  :- ").place(x=0,y=4)
        self.name_var = StringVar()
        self.name_entry = Entry(self.charge_master_main,width=31,textvariable=self.name_var)
        self.name_entry.focus()
        self.name_entry.place(x=82,y=1,height=30)
        #dept section 

        Label(self.charge_master_main,text="Department :-").place(x=0,y=42)
        
        #department dropdown 


      
        try:
            self.dept_var = StringVar() # var of dropdown
            self.dept_menu = Combobox(self.charge_master_main,textvariable = self.dept_var)
            self.dept_menu['values']=  ['Select'] #this list will come from database
            self.name_entry.bind("<Return>",lambda f:self.dept_menu.focus())


            #get department from database 
            val = ['Select']
            try:
                cur.execute("select name,id from department")
                for i in cur.fetchall():
                   val.append(i[0]+" - "+str(i[1]))
                   self.dept_id_lst.append(i[1])
               
                if len(val)>1:
                    self.dept_menu['values']=val
                else:
                    messagebox.showerror("!","Please enter department first...",parent=self.charge_master_main)
            except:
                messagebox.showerror("Error","can not able to fetch department...",parent=self.charge_master_main)
                        


            self.dept_menu.set("Select")
            self.dept_menu['state']='readonly'
            self.dept_menu.config(width=28)
            self.dept_menu.place(x=82,y=35,height=30)

        except Exception as e:
            print(e+"line no 52")
            messagebox.showerror("No Department Found","Please Enter Department First")

        
       

        #old case and net case 

        Label(self.charge_master_main,text="New Case  :-").place(x=0,y=72)
        self.new_case_var=IntVar()
        self.new_case_entry = Entry(self.charge_master_main,width=10,textvariable=self.new_case_var)
        self.new_case_entry.place(x=80,y=70,height=28)

        Label(self.charge_master_main,text="Old Case").place(x=170,y=72)
        self.old_case_var = IntVar()
        self.old_case_entry = Entry(self.charge_master_main,width=10,textvariable=self.old_case_var)
        self.old_case_entry.place(x=230,y=70,height=28)
        

        self.dept_menu.bind("<Return>",lambda f:self.set_focus(self.new_case_entry,self.new_case_var))
        self.new_case_entry.bind("<Return>",lambda f:self.set_focus(self.old_case_entry,self.old_case_var))
        self.old_case_entry.bind("<Return>",lambda f:self.add_to_db())
    
        col = ['id','fee_name','new_case','old_case','dept_id']
        self.tree = Treeview(self.charge_master_main,column=col,show='headings',height=17)

        self.tree.heading('id',text="FID")
        self.tree.heading('fee_name',text="Fee/Charge Name")
        self.tree.heading('new_case',text="NewCase")
        self.tree.heading('old_case',text="OldCase")
        self.tree.heading('dept_id',text="DeptId")

        self.tree.column('0',width=30)
        self.tree.column('1',width=120)
        self.tree.column('2',width=50)
        self.tree.column('3',width=50)
        self.tree.column('4',width=30)
    
        self.tree.place(x=0,y=135)

        scrollbar = Scrollbar(self.charge_master_main,orient=VERTICAL,command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=316,y=135,height=400)

      

        self.display_data()
        
        #add 
        self.add = Button(self.charge_master_main,width=15,text="Add",command=self.add_to_db)
        self.add.place(x=105,y=100)

        self.edit = Button(self.charge_master_main,width=8,text="Edit",command=self.update_record)
        self.edit.place(x=20,y=540)

        self.clear = Button(self.charge_master_main,width=15,text="Clear",command=self.clear_selection)


        #delete
        self.delete = Button(self.charge_master_main,width=8,text="Delete",command=self.delete_record)
        self.delete.place(x=110,y=540)

        #disable by default
        self.edit['state']='disable'
        self.delete['state']='disable'

        #exit
        self.exit = Button(self.charge_master_main,width=8,text="Exit",command=self.charge_master_main.destroy)
        self.exit.place(x=200,y=540)
        
        #shortcut label 
        Label(self.charge_master_main,text="ctrl+d").place(x=135,y=578)
        Label(self.charge_master_main,text="ctrl+e").place(x=40,y=578)
        Label(self.charge_master_main,text="esc").place(x=224,y=578)

        #bind edit,delete,esc
        self.charge_master_main.bind("<Control-d>",self.ctrl_d)
        self.charge_master_main.bind("<Control-e>",self.ctrl_e)
        self.charge_master_main.bind("<Escape>",lambda e:self.charge_master_main.destroy())

        self.charge_master_main.bind("<<TreeviewSelect>>",self.get_selection)
        self.charge_master_main.mainloop()

    def get_selection(self,e):
        self.des = 1 #set to 1 for editing mode on 
        self.edit['state']='normal'
        self.delete['state']='normal'
        values = []
        for item in self.tree.selection():
            values = self.tree.item(item,'values')
        
        
        if len(values)>0 and len(values)>3:
            try:
                self.name_var.set(values[1])
                try:
                    self.dept_var.set(self.dept_menu['values'][self.dept_id_lst.index(int(values[4]))+1])
                except ValueError:
                    messagebox.showerror("Error","cannot find department with this particular id",parent=self.charge_master_main)
                self.new_case_var.set(int(values[2]))
                self.old_case_var.set(int(values[3]))
            
                self.clear.place(x=105,y=100)

            except Exception as e:
                print(e)

      
    def clear_selection(self):
        for i in self.tree.selection():
            self.tree.selection_remove(i)

        self.charge_master_main.update()
        self.edit['state']='disable'
        self.delete['state']='disable'

        self.name_var.set("")
        self.dept_var.set(self.dept_menu['values'][0])
        self.new_case_var.set(0)
        self.old_case_var.set(0)
        self.des=0
        self.name_entry.focus()
        self.clear.place_forget()

    def add_to_db(self):
        if self.des ==0 : #check if des == 0 then it is in add mode else if des == 1 then itis in edit mode 
            self.add['state']='disable'
            try:
                name  = str(self.name_var.get()).replace("'","").replace('"','').strip()
                dept_nm = str(self.dept_var.get()).replace("'","").replace('"','').strip() 
                if dept_nm !="Select":
                    if name !="" :
                        try:
                            index = self.dept_menu['values'].index(dept_nm)
                            dept_id = self.dept_id_lst[index-1]
                        except Exception as e:
                            print(e)
                            self.add['state']='normal'
                            messagebox.showerror("!","can not find department id",parent=self.charge_master_main)
                            return
                        try:
                            new_case_fee =  int(str(self.new_case_var.get()).replace("'","").replace('"','').strip())
                            old_case_fee = int(str(self.old_case_var.get()).replace("'","").replace('"','').strip())
                        except:
                            self.add['state']='normal'
                            messagebox.showerror("New  Fees / Old Fees","Invalid input for fees ",parent=self.charge_master_main)
                            return 
                        cur.execute(f"insert into charge(name,dep_id,new_case_fee,old_case_fee) values('{name}',{dept_id},{new_case_fee},{old_case_fee})")
                        con.commit()
                        messagebox.showinfo("Success","Charges added succesfully",parent=self.charge_master_main)
                        self.name_var.set("")
                        self.dept_var.set("Select")
                        self.new_case_var.set(0)
                        self.old_case_var.set(0)
                        self.display_data()
                        self.add['state']='normal'
                        self.name_entry.focus()
                    else: #else of blank name
                        self.add['state']='normal'
                        messagebox.showerror("Invalid input","Empty Fields",parent=self.charge_master_main)
                        return
                else: #else of select drop down
                    self.add['state']='normal'
                    messagebox.showerror("Error","Please Select department",parent=self.charge_master_main)
            except Exception as e:
                print(e)
                self.add['state']='normal'
                messagebox.showerror("Error while inserting charges","can not able to add new charges",parent=self.charge_master_main)        

    def update_record(self):
        res = messagebox.askquestion("?","Are you sure you want to update this charges ?",parent=self.charge_master_main)
        if res == "yes":
            self.edit['state'] = 'disable'
            values = []
            for item in self.tree.selection():
                values = self.tree.item(item,'values')

            name = str(self.name_var.get()).replace("'","").replace('"','').strip()
            dept_nm = str(self.dept_var.get()).replace("'","").replace('"','').strip()
            try:
                new_case = int(str(self.new_case_var.get()).replace("'","").replace('"','').strip())
                old_case = int(str(self.old_case_var.get()).replace("'","").replace('"','').strip())
            except :
                self.edit['state']='normal'
                messagebox.showerror("!","Invalid Input for fees (only accepted number not a-z)",parent=self.charge_master_main)
                return
            if dept_nm !="Select":
                if len(values)>0:
                    if name !="":
                        try:
                            index = self.dept_menu['values'].index(dept_nm)
                            dept_id = self.dept_id_lst[index-1]
                        except Exception as e:
                            print(e)
                            self.add['state']='normal'
                            messagebox.showerror("!","can not find department id",parent=self.charge_master_main)
                            return
                        try:
                            cur.execute(f"update charge set name='{name}',dep_id={dept_id},new_case_fee={new_case},old_case_fee={old_case} where id={values[0]} ")
                            con.commit()
                            messagebox.showinfo("Success","Charges Updated Successfully",parent=self.charge_master_main)
                            self.display_data()
                            self.clear_selection()
                        except:
                            messagebox.showerror("Error","can not able to update charges",parent=self.charge_master_main)
                    else:
                        self.edit['state']='normal'
                        messagebox.showerror("Invalid input","Empty Fields",parent=self.charge_master_main)
                        return
                else:
                    pass
            else:
                self.edit['state']='normal'
                messagebox.showwarning("!","Please select department ",parent=self.charge_master_main)
                return

    def delete_record(self):
        res = messagebox.askquestion("Are you sure?","really want to delete this charges ? ",parent=self.charge_master_main)
        if (res =="yes"):
            value  =[] #selected tree value
            for item in self.tree.selection():
                value = self.tree.item(item,'values')
            if len(value)>0:
                try:
                    cur.execute(f"delete from charge where id = {value[0]}")
                    con.commit()
                    messagebox.showinfo("!","charges deleted succesfully",parent=self.charge_master_main)
                    self.clear_selection()
                    self.display_data()
                except:
                    messagebox.showerror("there is something wrong !","cannot able to delete this charges ",parent=self.charge_master_main)

    def display_data(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            cur.execute("select id,name,new_case_fee,old_case_fee,dep_id from charge")
            for i in cur.fetchall():
                self.tree.insert('','end',text="",values=i)
        except:
            messagebox.showerror("Error","Cannot able to fetch charges")
    
    def set_focus(self,widget,widget_var):
        pos = len(str(widget_var.get())) 
        widget.focus()
        widget.icursor(pos)
    
    def ctrl_d(self,e):
        if self.des==1:
            self.delete_record()
        else:
            messagebox.showerror("Unable to delete charges","Please select charges that you want to delete",parent=self.charge_master_main)

    def ctrl_e(self,e):
        if self.des ==1:
            self.update_record()
        else:
            messagebox.showerror("Unable to edit charges","Please select charges that you want to edit",parent=self.charge_master_main)

    