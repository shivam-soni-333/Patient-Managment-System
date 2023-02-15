from tkinter import *
from tkinter.ttk import *
from db_con import con,cur
from tkinter import messagebox
import datetime
from reportlab.pdfgen import canvas
from ttkwidgets.autocomplete import AutocompleteCombobox
import os.path
import os
import win32api
import sys
from reportlab.lib.pagesizes import landscape,A5
import subprocess
import win32print

class case_entry(Toplevel):
    rowid= 0
    column = 0
    entryeditdes = 0 #used for only place one entry box when user double clicks on treeview 
    des = 0 # if des = 1 then user is in edit mode else user is in add mode 
    def __init__(self,master=None):
        super().__init__(master=master)
        self.main = self
        
        sys.setrecursionlimit(5000)
        self.main.title("Case Entry ")
        self.main.resizable(False,False)

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            



        window_height = 650
        window_width = 1050
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()-30 # - 30 for proper setting up screen on main window

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.main.focus_force()
        self.main.update()

        col = ["receipt_no","pat_nm","dep_id"] #self.tree_r stands for tree that display receipt details
        self.tree_r = Treeview(self.main,column = col ,show='headings',height=100)
        
        self.tree_r.heading("receipt_no",text="Receipt No.")
        self.tree_r.heading("pat_nm",text="Patient Name")
        self.tree_r.heading("dep_id",text="Dep Name")

        self.tree_r.column("receipt_no",width=30)
        self.tree_r.column("pat_nm",width=100)
        self.tree_r.column("dep_id",width=70)

        self.tree_r.place(x=0,y=0)
        self.tree_r.bind("<<TreeviewSelect>>",self.get_selection)
        
        
        
        scrollbar_r = Scrollbar(self.main, orient=VERTICAL, command=self.tree_r.yview)
        self.tree_r.configure(yscroll=scrollbar_r.set)
        scrollbar_r.place(x=244,y=10,height=630)


        #patient name 
        Label(self.main,text="Patient Name :- ").place(x=262,y=6)

        self.name_var = StringVar()
        self.name_entry = Entry(self.main,width=35,textvariable = self.name_var)
        self.name_entry.place(x=350,y=4)
        self.name_entry.focus()
        self.name_entry.bind("<Return>",self.change_to_address)

        #patient address

        Label(self.main,text="PatientAddress").place(x=260,y=40)

        self.address_var = StringVar()
        self.address_entry  = Entry(self.main,width=35,textvariable=self.address_var)
        self.address_entry.place(x=350,y=40,height=28)
        self.address_entry.bind("<Return>",self.change_to_age)
        
      
        #age 
        Label(self.main,text="Age").place(x=620,y=4)

        self.age_var = IntVar()
        self.age_entry = Entry(self.main,width=10,textvariable=self.age_var)
        self.age_entry.place(x=660,y=4)
        self.age_entry.bind("<Return>",self.change_to_case_no)
        
        #gender 
        Label(self.main,text="Gender :-").place(x=800,y=4)                
        
        self.gender_var = IntVar()
        self.gender_var.set(1)
        male = Radiobutton(self.main,text="Male",variable = self.gender_var,value=1)
        male.place(x=850,y=4)
        

        female = Radiobutton(self.main,text="Female",variable=self.gender_var,value=2)
        female.place(x=910,y=4)

        #case no 
        Label(self.main,text="Case No.").place(x=630,y=40)

        self.case_no_var = IntVar()
        self.case_no_entry = Entry(self.main,width=20,textvariable=self.case_no_var)
        self.case_no_entry.place(x=700,y=40,height=28)
        self.case_no_entry.bind("<Return>",self.change_to_doc_nm)

        #receipt no
        Label(self.main,text="Recipet No.").place(x=860,y=40)
        self.receipt_no_var = IntVar()
        self.receipt_no_entry = Entry(self.main,width=10,textvariable=self.receipt_no_var)
        self.receipt_no_entry.place(x=950,y=40,height=28)
        self.receipt_no_entry.bind("<Key>",lambda e:"break")
        
        #doctor name 
        Label(self.main,text="Doctor Name ").place(x=262,y=70)

        self.dr_name_lst = []
        self.dr_id_lst = []
        #get dr name from db
        try:
            cur.execute("select name,id from doctor")
            for i in cur.fetchall():
                self.dr_name_lst.append(i[0])
                self.dr_id_lst.append(i[1])
        except:
            messagebox.showinfo("!","please enter doctor to database")

        self.doctor_name_var  = StringVar()
        self.doctor_name_entry = AutocompleteCombobox(self.main,width=35,completevalues=self.dr_name_lst,textvariable=self.doctor_name_var)
        self.doctor_name_entry.place(x=350,y=70,height=28)
        self.doctor_name_entry.bind("<Return>",self.change_to_dept)
        #department 
        Label(self.main,text="Department Name :-").place(x=640,y=75)

        # self.department_name_var = StringVar()
        # self.department_name_entry = Entry(self.main,width=45,textvariable=self.department_name_var)
        # self.department_name_entry.place(x=720,y=70)

        self.department_name_var = StringVar()
        self.department_name = Combobox(self.main,textvariable = self.department_name_var,state='readonly',width=37)
        self.department_name['values']=  [] #this list will come from database
        self.department_name.place(x=750,y=70,height=28)

        #get departmet from database

        try:
            self.dep_name_lst = []
            self.dep_id_lst = []

            cur.execute("select name,id from department")
            for i in cur.fetchall():
                self.dep_name_lst.append(i[0])
                self.dep_id_lst.append(i[1])

            self.department_name['values']=self.dep_name_lst
            if len(self.dep_name_lst) > 0:
                self.department_name_var.set(self.department_name['values'][0])
            else:
                messagebox.showinfo("!","Please enter department",parent=self.main)
                return
        except:
            messagebox.showerror("Error","Can not find department in database",parent=self.main)
        
        self.department_name.bind("<Return>",self.change_to_date)
        #date 
        Label(self.main,text="Date :- ").place(x=820,y=110)

        self.date_var = StringVar(value=str(datetime.datetime.today().strftime('%d/%m/%Y'))) # all over we are using same date format dd/mm/yy  
        self.date_entry = Entry(self.main,width=20,textvariable=self.date_var)
        self.date_entry.place(x=870,y=105,height=27)
        # self.date_entry.configure(state='disabled')
        self.date_entry.bind("<FocusOut>",self.check_date)

        
        
      
        #current year
        self.current_year_lbl = Label(self.main,text="")
        self.current_year_lbl.place(x=450,y=110)
        try:
            cur.execute("select start_date,end_date from year where is_current_year=1")
            out = cur.fetchone()
            if out != None:
                start_date = out[0]
                end_date = out[1]

                self.current_year_lbl['text'] = "Current Year "+str(start_date)+" "+str(end_date)

            else:
                raise Exception
        except:
            pass
        #tree
        col = ['charge_name','rate_of_charge','no_of_times','total']
        self.tree = Treeview(self.main,columns=col,show='headings')
        
        self.tree.column('charge_name',width=250,anchor='center')
        self.tree.column('rate_of_charge',width=130,anchor='center')
        self.tree.column('no_of_times',width=130,anchor='center')
        self.tree.column('total',width=130,anchor='center')

        
        self.tree.heading("charge_name",text="Charge Name")
        self.tree.heading("rate_of_charge",text="Rate of charge")
        self.tree.heading("no_of_times",text="No of times")
        self.tree.heading("total",text="Total")

        self.tree.place(x=262,y=130,height=350)
        self.tree.insert('','end',text="",values = ("#",0,0,0))
        self.tree.focus(self.tree.get_children()[0])
        self.tree.selection_set(self.tree.get_children()[0])
        self.tree.bind('<Return>',self.set_cell_value)
        
        self.date_entry.bind("<Return>",self.set_tree_focus)

        scrollbar = Scrollbar(self.main,orient=VERTICAL,command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=928,y=134,height=344)

    
      
       
        #add new row
        Label(self.main,text="Ctrl + a").place(x=960,y=210)
        self.add_row_btn=Button(self.main,text="AddCharge",command=self.add_row,width=12)
        self.add_row_btn.place(x=940,y=230,height=30)

        #delete row
        Label(self.main,text="Ctrl + d").place(x=965,y=300)
        self.delete_row_btn = Button(self.main,text="DeleteCharge",command=self.delete_row,width=12)
        self.delete_row_btn.place(x=940,y=270,height=30)

        #token_no  
        Label(self.main,text="Token No :-").place(x=262,y=504)

        self.token_no_var = IntVar()
        self.token_no_entry = Entry(self.main,width=10,textvariable=self.token_no_var)
        self.token_no_entry.place(x=330,y=500)

        

        #payment_by 
        Label(self.main,text="Payment By :-").place(x=440,y=505)

        self.payment_var = StringVar()
        self.payment_menu = Combobox(self.main,textvariable = self.payment_var,state='readonly')
        self.payment_menu['values']=  ['CASH','CHEQUE','POS'] #this list will come from database
        self.payment_var.set(self.payment_menu['values'][0])
        self.payment_menu.place(x=530,y=500)

        #sub_total
        Label(self.main,text="Sub Total").place(x=715,y=505)

        self.sub_total_var = IntVar()
        self.sub_total_entry = Entry(self.main,width=20,textvariable=self.sub_total_var)
        self.sub_total_entry.place(x=780,y=500)



        #discount
        Label(self.main,text="Discount").place(x=715,y=535)

        self.discount_var = IntVar()
        self.discount_entry = Entry(self.main,width=20,textvariable=self.discount_var)
        self.discount_entry.place(x=780,y=530)
        self.discount_entry.bind("<FocusOut>", self.discount)
        
        #total
        Label(self.main,text="Grand Total").place(x=710,y=565)

        self.total_var = IntVar()
        self.total_entry = Entry(self.main,width=20,textvariable=self.total_var)
        self.total_entry.place(x=780,y=560)

        #add
        self.add = Button(self.main,text="Add",width=15,command=self.add_to_db)
        self.add.place(x=350,y=600,height=40)
        Label(self.main,text="Ctrl+i").place(x=350,y=580)

        #edit
        self.edit = Button(self.main,text="Edit",width=15,command=self.update_record)
        self.edit.place(x=500,y=600,height=40)
        self.edit['state']='disable'
        Label(self.main,text="Ctrl+e").place(x=500,y=580)
        
        #print
        self.print = Button(self.main,text="Print",width=15,command=self.print_receipt)
        self.print.place(x=650,y=600,height=40)
        Label(self.main,text="Ctrl+p").place(x=650,y=580)
        # self.print['state'] = 'disable'
        #exit
        self.exit = Button(self.main,text="Exit",width=15,command=self.exit_f)
        self.exit.place(x=800,y=600,height=40) 

        #clear
        self.clear_btn = Button(self.main,text="Clear",width=15,command=self.clear)
     
        #shortcut for male femal
        
        Label(self.main,text="Ctrl+m for male").place(x=950,y=400)
        Label(self.main,text="Ctrl+f for female").place(x=950,y=420)

        #calling functions ... 
        self.display_data()
        self.calculate_total()
        self.get_next_receipt_no()
        self.get_next_token_no()
        self.case_no_var.set(self.token_no_var.get())


        tab_order_lst = (self.name_entry,self.address_entry,self.age_entry,self.case_no_entry,self.doctor_name_entry,self.department_name,self.date_entry,self.tree,self.print,self.token_no_entry,self.payment_menu)

        for widget in tab_order_lst:
            widget.lift()
        
        #event binding with main window

        self.department_name.bind('<<ComboboxSelected>>',self.get_next_receipt_no)
        self.main.bind("<Escape>",self.exit_f)
        self.main.bind("<Control-p>",self.ctrl_p)
        self.main.bind("<Control-a>",self.add_row)
        self.main.bind("<Control-d>",self.delete_row)
        self.main.bind("<Control-m>",self.select_male)
        self.main.bind("<Control-f>",self.select_female)
        self.main.bind("<Control-i>",self.add_to_db)
        self.main.bind("<Control-e>",self.update_record_call)
        

        self.main.mainloop()

    
    def set_cell_value(self,e):
        if len(self.tree.selection()) == 0:
            messagebox.showerror("!","Please Select Row",parent=self.main)
            return    
        
        for item in self.tree.selection():
            self.item_text = self.tree.item(item,'values')
    
        
        try:
            self.charge_name_lst = [] #this will come from database
            self.charge_id_lst = []
            self.rate_of_charge_lst = []
            cur.execute("select name,id,new_case_fee from charge")
            for i in cur.fetchall():
                self.charge_name_lst.append(i[0])
                self.charge_id_lst.append(i[1])  
                self.rate_of_charge_lst.append(i[2])          
        except Exception as e:
            print(e)
            # messagebox.showinfo("!","Please add some charges")

        self.charge_name_var  = StringVar()
        self.charge_name_entry = AutocompleteCombobox(self.main,width=30,validate="focusout",completevalues=self.charge_name_lst,textvariable=self.charge_name_var)
        self.charge_name_entry.place(x=280,y=440)
        self.charge_name_entry.focus()
        if self.item_text[0] != "#":
            self.charge_name_var.set(self.item_text[0])
        self.charge_name_entry.bind("<FocusOut>",self.set_rate_of_charge)
        self.charge_name_entry.bind("<Return>",self.set_rate_of_charge)
        self.charge_name_entry.bind('<Right>',lambda e:self.rate_entry.focus())
        

        self.rate_var =DoubleVar()
        self.rate_entry = Entry(self.main,width=8,validate="focusout",textvariable=self.rate_var)
        self.rate_entry.place(x=600,y=440)
        self.rate_entry.bind("<Return>",self.change_to_no_of_times)
        if self.item_text[1] != '0':
            self.rate_var.set(self.item_text[1])
        self.rate_entry.bind("<Right>",lambda e:self.no_of_time_entry.focus())

        self.no_of_time = IntVar()
        self.no_of_time_entry = Entry(self.main,width=8,validate='focusout',textvariable=self.no_of_time)
        self.no_of_time_entry.place(x=700,y=440)
        self.no_of_time_entry.bind("<Return>",self.count_total)
        self.no_of_time_entry.bind("<FocusOut>",self.count_total)
        if self.item_text[2] != '0': 
            self.no_of_time.set(self.item_text[2])
        self.no_of_time_entry.bind("<Right>",lambda e:self.total_entry.focus())

        self.total_tree_var = DoubleVar()
        self.total_entry_tree = Entry(self.main,width=8,validate='focusout',textvariable=self.total_tree_var)
        self.total_entry_tree.place(x=800,y=440)
        self.total_entry_tree.bind("<Return>",self.set_value)
        self.total_entry_tree.bind("<FocusOut>",self.set_value)
        if self.item_text[3] != '0"' or self.item_text[3] != '0.0':
            self.total_tree_var.set(self.item_text[3])

    
        
    def set_rate_of_charge(self,e):
        charge_name = self.charge_name_var.get()
        
        try:
            index = self.charge_name_lst.index(charge_name)
            rate = self.rate_of_charge_lst[index]
            self.rate_var.set(rate)
        except Exception as e:
           print(e)
       
        l = len(str(self.rate_var.get()))
        self.rate_entry.focus()
        self.rate_entry.icursor(l)
    
    def change_to_no_of_times(self,e):
        try:
            rate = float(self.rate_var.get())
        except:
            messagebox.showerror("!","Invalid Input",parent=self.main)
            return
        l = len(str(self.no_of_time.get()))
        self.no_of_time_entry.focus()
        self.no_of_time_entry.icursor(l)
    
    def count_total(self,e):
        try:
            rate = float(self.rate_var.get())
            no_of_times = int(self.no_of_time.get())
            total = rate * no_of_times
            self.total_tree_var.set(total)
        except:
            messagebox.showerror("!","Invalid Data",parent=self.main)
            return



        l = len(str(self.total_var.get()))
        self.total_entry_tree.focus()
        self.total_entry_tree.icursor(l)
    

    def set_value(self,e):
        try:
            charge_name =self.charge_name_var.get()
            rate = self.rate_var.get()
            no_of_times = self.no_of_time.get()
            total = self.total_tree_var.get()
        except:
            messagebox.showerror("!","Invalid Input",parent=self.main)
            return
        
        t = (charge_name,rate,no_of_times,total) # tuple 
        try:
            item = self.tree.selection()[0]
            self.tree.set(item,column=0,value=charge_name)
            self.tree.set(item,column=1,value=rate)
            self.tree.set(item,column=2,value=no_of_times)
            self.tree.set(item,column=3,value=total)
            
            self.charge_name_entry.destroy()
            self.rate_entry.destroy()
            self.no_of_time_entry.destroy()
            self.total_entry_tree.destroy()
            
           
            
            self.tree.focus_force()
            self.tree.selection_set(item)
            self.calculate_total()
        except:
            messagebox.showerror("!","Can not able to set values",parent=self.main)
            return
            

        

    def add_row(self,e=None):
        try:
            self.add_row_btn['state'] = 'disable'
            self.tree.insert("","end",id=self.next_row_id(),values=("#",0,0,0))
            self.add_row_btn['state'] = 'normal'
            self.calculate_total()
            child = self.tree.get_children()
            self.tree.focus_force()
            if child:
                self.tree.focus(child[-1])
                self.tree.selection_set(child[-1])

        except:
            messagebox.showerror("!","Can not able to add row",parent=self.main)
    
    def delete_row(self,e=None):
        try:
            self.delete_row_btn['state'] = 'disable'
            selected_item = self.tree.selection()[0] ## get selected item
            self.tree.delete(selected_item)
            self.delete_row_btn['state'] = 'normal'
            self.calculate_total()
            self.tree.focus_force()
            child = self.tree.get_children()
            if child:
                self.tree.focus(child[-1])
                self.tree.selection_set(child[-1])

        except:
            messagebox.showerror("!","Can not delete row",parent=self.main)
            self.delete_row_btn['state'] = 'normal'


    def calculate_total(self):
        total = 0.0
        for child in self.tree.get_children():
            try:
                total+=float(self.tree.item(child,'values')[3])
            except:
                pass
        total= round(total,2)
        self.sub_total_var.set(total)
        self.total_var.set(round(total-self.discount_var.get(),2))

    def discount(self,e):
        try:
            dis = float(self.discount_var.get())
            sub_total = float(self.sub_total_var.get())
            if dis < sub_total :
                grand_total = sub_total - dis
                grand_total = round(grand_total,2)
                self.total_var.set(grand_total)
            else:
                messagebox.showerror("!","Discount can not be greater than total",parent=self.main)
                self.discount_var.set(0)
                return
        except Exception as e:
            self.discount_var.set(0)
            messagebox.showerror("!","Invalid data",parent=self.main)

    def next_row_id(self):
        self.rowid+=1
        return self.rowid
    

    def add_to_db(self,des=None,e=None):
        if self.des == 0: #check if des =0 then user is in add mode else user is in edit mode
            self.add['state']='disable'
            tree_data_lst= []

            for item in self.tree.get_children():
                if self.tree.item(item,'values')[0] != '#':
                    if self.tree.item(item,'values')[0] != "":
                        tree_data_lst.append(self.tree.item(item,'values'))
                    else:
                        messagebox.showwarning("!","charge name should not be blank",parent=self.main)
                        self.add['state']='normal'
                        return -1
                else:
                    messagebox.showwarning("!","Empty Charges ( # not allowed as  charge name )",parent=self.main)
                    self.add['state']='normal'
                    return -1
                        

            patient_name = str(self.name_var.get()).replace("'","").replace('"','').strip()
            patient_address = str(self.address_var.get()).replace("'","").replace('"','').strip()
            try:
                age = int(self.age_var.get())
            except:
                self.add['state']='normal'
                messagebox.showerror("!","invalid input for age",parent=self.main)
                return -1
            gender = self.gender_var.get()
            if gender == 1:
                gender ="male"
            else :
                gender = "female"
            
            try:
                case_no = int(self.case_no_var.get())
            except:
                self.add['state']='normal'
                messagebox.showerror("!","Invalid input for case no")
                return -1
            
            try:
                receipt_no = int(self.receipt_no_var.get())
            except:
                self.add['state']='normal'
                messagebox.showerror("!","Invalid input for receipt no",parent=self.main)
                return -1

            
            
            doc_name =  str(self.doctor_name_var.get()).replace("'","").replace('"','').strip()

            try:
                dep_name = str(self.department_name_var.get()).strip()
                index = self.dep_name_lst.index(dep_name)
                deptid = self.dep_id_lst[index]
            except:
                self.add['state']='normal'
                messagebox.showerror("!","Something wrong while getting department id",parent=self.main)
                return

            date = str(self.date_var.get()).replace("'","").replace('"','').strip()
            self.check_date()

            #token_no 
            try:
                token_no =int(self.token_no_var.get())
            except Exception as e:
                print(e)
                self.add['state']='normal'
                messagebox.showerror("!","Invalid token no",parent=self.main)
                return -1

            #payment_method 
            try:
                payment_method = str(self.payment_var.get()).strip()
            except:
                self.add['state']='normal'
                return -1

            #subtotal
            try:
                sub_total = float(self.sub_total_var.get())
            except:
                self.add['state']='normal'
                messagebox.showerror("!","invalid input for subtotal",parent=self.main)
                return -1
            #discount 
            try:
                discount = float(self.discount_var.get())
            except:
                self.add['state']='normal'
                messagebox.showerror("!","invalid input for discount ",parent=self.main)
                return -1
            #grand total
            try:
                grand_total = float(self.total_var.get())
            except:
                messagebox.showerror("!","invalid input for grand total",parent=self.main)
                self.add['state']='normal'
                return -1
            
            #add to db main function starts from here :)
            if(patient_name != "" and patient_address !="" and doc_name != ""):
                try:
                    cur.execute(f"insert into patient(name,address,age,gender) values('{patient_name}','{patient_address}',{age},'{gender}')")
                    pid = int(cur.lastrowid)
                    cur.execute("select * from year where is_current_year=1")
                    out = cur.fetchone()
                    if out != None:
                        id = out[0]
                        start_date = datetime.datetime.strptime(out[1],'%d/%m/%Y')
                        end_date = datetime.datetime.strptime(out[2],'%d/%m/%Y')
                        date_obj = datetime.datetime.strptime(date,'%d/%m/%Y')
                        if date_obj >= start_date and date_obj <= end_date:
                            cur.execute(f"select receipt_no from manage_receipt_no where year = {id} and dept_id = {deptid}")
                            receipt_no = cur.fetchone()
                            if receipt_no != None:
                                receipt_no = receipt_no[0]
                                cur.execute(f"insert into receipt(receipt_no,pid,date,doc_name,case_no,token_no,pay_method,sub_total,discount,grand_total,year,dept_id) values({receipt_no},{pid},'{date}','{doc_name}','{case_no}','{token_no}','{payment_method}','{sub_total}','{discount}','{grand_total}','{id}',{deptid})")
                                receipt_id = cur.lastrowid
                                for i in tree_data_lst:
                                    cur.execute(f"insert into receipt_charge(receipt_id,name,rate,no_of_times,total,year) values({receipt_id},'{i[0]}',{i[1]},{i[2]},{i[3]},'{id}')")
                                cur.execute(f"update manage_receipt_no set receipt_no= receipt_no+1 where year = {id} and dept_id = {deptid} ") #increment receipt no as final receipt was made
                                cur.execute(f"update token_no set token_no = token_no+1 where date='{date}'")
                            else: #if receipt_no of particualr year is not present
                                messagebox.showerror("Current Year Error","Please enter current year in year master",parent=self.main)
                                self.add['state']='normal'
                                return -1
                            con.commit()
                            if des  == None:
                                messagebox.showinfo("Success","Receipt Saved",parent=self.main)
                            self.display_data()
                            if des == None:
                                self.clear()
                            self.add['state']='normal'
                        else:
                            messagebox.showerror("Invalid date","date is not in current year  range",parent=self.main)
                            self.add['state']='normal'
                            return -1
                except Exception as e:  
                    print(e)
                    messagebox.showerror("error in receipt creation","There is something wrong while creating receipt ",parent=self.main)
                    self.add['state']='normal'
                    return -1
                #end add to db function
            else:
                messagebox.showerror("Invalid input","Empty input",parent=self.main)
                self.add['state']='normal'
                return -1
                
    def display_data(self):
        self.tree_r.delete(*self.tree_r.get_children()) #get all child of tree
        try:
            cur.execute("select id from year where is_current_year=1")
            out = cur.fetchone()
            if out != None:
                self.yearid = out[0] 
            else:
                pass
        except:
            messagebox.showerror("!","can not able to display data",parent=self.main)
            
        
        try:
            cur.execute(f"select receipt_no,pid,dept_id from receipt where year={self.yearid}")
            for i in cur.fetchall():
                cur.execute(f"select name from patient where id={i[1]}")
                res  = cur.fetchone()
                cur.execute(f"select name from department where id={i[2]}")
                res2= cur.fetchone()
                if res != None and res2 != None:
                    self.tree_r.insert("","end",values=(i[0],res[0],res2[0]))
        except Exception as e:
            print(e)
            messagebox.showerror("!","Cannot fetch receipt from database",parent=self.main)
            
    
    def clear(self):
        self.name_var.set('')
        self.address_var.set('')
        self.age_var.set(0)
        self.doctor_name_var.set("")
        self.department_name_var.set(self.dep_name_lst[0])
        self.get_next_receipt_no()
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("","end",values=("#",0,0,0))
        self.tree.focus(self.tree.get_children()[0])
        self.tree.selection_set(self.tree.get_children()[0])

        self.get_next_token_no()
        self.case_no_var.set(self.token_no_var.get())
        self.sub_total_var.set(0)
        self.discount_var.set(0)
        self.des = 0
        self.total_var.set(0)
        self.repid= -1
        self.pid = -1
        for item in self.tree_r.selection():
            self.tree_r.selection_remove(item)
        self.name_entry.focus()
        
        self.main.update()
        self.edit['state']  = 'disable'
        
        self.clear_btn.place_forget()


        
    
    def get_next_receipt_no(self,e=None):
        #get receipt_no from db 
        try:
            date  = self.date_var.get()
            date_obj = datetime.datetime.strptime(date,'%d/%m/%Y')
            dept_name = self.department_name_var.get()
            index = self.dep_name_lst.index(dept_name)
            dept_id = self.dep_id_lst[index]
            cur.execute("select * from year where is_current_year=1")
            out = cur.fetchone()
            if out != None:
                start_date = out[1]
                end_date = out[2]
                start_date = datetime.datetime.strptime(start_date,'%d/%m/%Y')
                end_date = datetime.datetime.strptime(end_date,'%d/%m/%Y')
                if date_obj >= start_date and date_obj <= end_date:
                    cur.execute(f"select receipt_no from manage_receipt_no where year={out[0]} and dept_id = {dept_id}")
                    out2 = cur.fetchone()
                    if out2 != None:
                        self.receipt_no_var.set(out2[0])
                    else:
                        messagebox.showerror("!","can not find receipt no of current year",parent=self.main)
                        return
                else:
                    messagebox.showerror("Invalid date","Date is not in range of current year",parent=self.main)
            else:
                messagebox.showerror("Empty year master!","enter current year in year master",parent=self.main)
        except Exception as e:
            print(e)
            messagebox.showerror("!","cannot find receipt no from database",parent=self.main)

    def get_next_token_no(self):
        #get token no from database
        try:   
            date = str(self.date_var.get())
            year = date[6:] 
            cur.execute("select * from year where is_current_year=1 ")
            out = cur.fetchone()
            if out != None:
                start_date = out[1]
                end_date = out[2]
                start_date = datetime.datetime.strptime(start_date,"%d/%m/%Y")
                end_date = datetime.datetime.strptime(end_date,"%d/%m/%Y")
                try:
                    date_obj = datetime.datetime.strptime(date,"%d/%m/%Y")
                except:
                    messagebox.showerror("Error","Day is out of range of month",parent=self.main)
                    return

                if date_obj >=start_date and date_obj<= end_date:
                    cur.execute(f"select token_no from token_no where date='{date}'")
                    out = cur.fetchone()
                    if out != None:
                        self.token_no_var.set(out[0])
                        self.case_no_var.set(out[0])
                    else:
                        cur.execute(f"insert into token_no(date,token_no) values('{date}',1)")
                        con.commit()
                        self.token_no_var.set(1)
                        self.case_no_var.set(1)
                else:
                    self.date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
                    messagebox.showerror("date is not range of current year","Invalid date",parent=self.main)
                    return
            else:
                self.date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
                messagebox.showerror("Year Not Found","Please enter current year in year master",parent=self.main)
                return 
        except Exception as e :
            print(e)
            messagebox.showerror("!","can not find token no ",parent=self.main)
            self.token_no_var.set(0)
            self.case_no_var.set(0)

    def check_date(self,e=None):
        try:
            date= str(self.date_var.get())
            yy =date[6:]
            try:
                dd = int(date[0:2])
                mm  = int(date[3:5])
            except:
                self.date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
                messagebox.showerror("Invalid date","Make sure date in format of DD/MM/YYYY ",parent=self.main)
                return 
           
            if dd <=31 and mm <=12 and len(yy)==4:
                self.get_next_receipt_no()
                self.get_next_token_no()
            else:
                self.date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
                messagebox.showerror("Invalid date","Date must be in DD/MM/YYYY format",parent=self.main)
        except Exception as e:
            pass
    
    def get_selection(self,e):
        self.edit['state'] = 'normal'
        self.print['state']  = 'normal'
        self.clear_btn.place(x=350,y=600,height=40)
        self.des=1
        values  = []
        for item in self.tree_r.selection():
            values = self.tree_r.item(item,'values')
        if len(values) > 0:
            self.old_receipt_no = values[0]
            name = values[1]
            dept_name = values[2]
            cur.execute("select id from year where is_current_year=1")
            year_id = cur.fetchone()
            cur.execute(f"select id from department where name = '{dept_name}' ")
            dept_id = cur.fetchone()
            if year_id != None and dept_id != None:
                self.year_id = year_id[0]
                dept_id=dept_id[0]
                cur.execute(f"select * from receipt where receipt_no = {self.old_receipt_no} and year={self.year_id} and dept_id={dept_id}")
                out = cur.fetchone()
                if out != None:
                    self.repid =  out[0] #this will use while editing
                    self.receipt_no_var.set(out[1])
                    self.pid = out[2] #this will use while editing
                    self.date_var.set(out[3])
                    self.doctor_name_var.set(out[4])
                    self.case_no_var.set(out[5])
                    token_no = out[6]
                    self.token_no_var.set(token_no)
                    pay_method = out[7]
                    self.payment_var.set(pay_method)
                    sub_total = out[8]
                    self.sub_total_var.set(sub_total)
                    discount = out[9]
                    self.discount_var.set(discount)
                    grand_total = out[10]
                    self.total_var.set(grand_total)
                    year = out[11]
                    self.old_dep_id = out[12]
                    try:
                        cur.execute(f'select name from department where id={self.old_dep_id}')
                        out = cur.fetchone()
                        if out != None:
                            self.department_name_var.set(out[0])
                        else:
                            raise Exception
                    except Exception as e:
                        print(e)
                        messagebox.showerror("!","Can not find department name",parent=self.main)

                    cur.execute(f"select * from patient where id = {self.pid}")
                    patient_info = cur.fetchone()
                    if patient_info != None:
                        self.name_var.set(patient_info[1])
                        self.address_var.set(patient_info[2])
                        self.age_var.set(patient_info[3])
                        if patient_info[4] == "male" or patient_info[4] == "MALE":
                            self.gender_var.set(1)
                        else:
                            self.gender_var.set(2)
                    else:
                        messagebox.showerror("!","Can not find patient information",parent=self.main)

                    cur.execute(f"select name,rate,no_of_times,total from receipt_charge where receipt_id = {self.repid}")
                    self.tree.delete(*self.tree.get_children())
                    for i in cur.fetchall():
                        self.tree.insert("",'end',values=i)
                    
                    child = self.tree.get_children()
                    if child:
                        self.tree.focus(child[0])
                        self.tree.selection_set(child[0])

                else:
                    messagebox.showerror("!","cannot able to find receipt details",parent=self.main)
            else:
                messagebox.showerror("!","Cannot find year in year master",parent=self.main)

    def update_record(self):
        res = messagebox.askquestion("Are you sure?","do you really want to update this record ? ",parent=self.main)
        if res == "yes":
            if self.des == 1: #check if des = 0 then user is in edit mode else user is in add mode
                self.edit['state']='disable'

                try:
                    name  = str(self.name_var.get()).replace("'","").replace('"','').strip()
                    address = str(self.address_var.get()).replace("'","").replace('"','').strip()
                except Exception as e:
                    print(e)
                

                try:
                    age = int(self.age_var.get())
                except:
                    messagebox.showerror("!","Invalid age",parent=self.main)
                    self.edit['state']='normal'
                    return
                
                gender = self.gender_var.get()
                if gender == 1:
                    gender ="male"
                else :
                    gender = "female"
                
                try:
                    case_no = int(self.case_no_var.get())
                except:
                    self.edit['state']='normal'
                    messagebox.showerror("!","Invalid case no",parent=self.main)
                    return
                
                try:
                    receipt_no = int(self.receipt_no_var.get())
                except:
                    self.edit['state']='normal'
                    messagebox.showerror("!","Invalid input for receipt no",parent=self.main)
                    return
                
                doc_name =  str(self.doctor_name_var.get()).replace("'","").replace('"','').strip()

                try:
                    dep_name = str(self.department_name_var.get()).strip()
                    index = self.dep_name_lst.index(dep_name)
                    depid = self.dep_id_lst[index]
                except:
                    self.edit['state']='normal'
                    messagebox.showerror("!","Something wrong while getting department id",parent=self.main)
                
                date = str(self.date_var.get()).replace("'","").replace('"','').strip()
                self.check_date()

                #token_no 
                try:
                    token_no =int(self.token_no_var.get())
                except Exception as e:
                    print(e)
                    self.edit['state']='normal'
                    messagebox.showerror("!","Invalid token no",parent=self.main)
                    return

                #payment_method 
                try:
                    payment_method = str(self.payment_var.get()).strip()
                except:
                    self.edit['state']='normal'
                    return 

                #subtotal
                try:
                    sub_total = float(self.sub_total_var.get())
                except:
                    self.edit['state']='normal'
                    messagebox.showerror("!","invalid input for subtotal",parent=self.main)
                    return
                #discount 
                try:
                    discount = float(self.discount_var.get())
                except:
                    self.edit['state']='normal'
                    messagebox.showerror("!","invalid input for discount ",parent=self.main)
                    return 
                #grand total
                try:
                    grand_total = float(self.total_var.get())
                except:
                    messagebox.showerror("!","invalid input for grand total",parent=self.main)
                    self.edit['state']='normal'
                    return
                
                #get charges data from treeview
                tree_data_update_lst = []
                
                for item in self.tree.get_children():
                    if self.tree.item(item,'values')[0] != '#':
                        if self.tree.item(item,'values')[0] != "":
                            tree_data_update_lst.append(self.tree.item(item,'values'))
                        else:
                            messagebox.showwarning("!","charge name should not be blank",parent=self.main)
                            self.edit['state']='normal'
                            return 
                    else:
                        messagebox.showwarning("!","Empty Charges ( # not allowed as  charge name )",parent=self.main)
                        self.edit['state']='normal'
                        return 
            
                

                if(name != "" and address !="" and doc_name != ""):
                    try:
                        if self.repid != -1 and self.pid != -1: #if this will -1 then use not selected any entry from treeview (as this will set accordingly in get_selection function that will callup when treeview selected)
                            cur.execute(f"update patient set name='{name}',address='{address}',age={age},gender='{gender}' where id={self.pid}")
                            cur.execute(f"select * from year where is_current_year=1")
                            out = cur.fetchone()
                            if out != None:
                                yearid= out[0]
                                if self.old_dep_id == depid: # if department was same then no need to change receipt no 
                                    cur.execute(f"update receipt  set doc_name = '{doc_name}', case_no ={case_no} ,token_no = {token_no},pay_method='{payment_method}',sub_total = {sub_total},discount={discount},grand_total = {grand_total} ,date='{date}',year={yearid} where id = {self.repid} ")
                                else: #if deparment was changed then need to change receipt no 
                                    cur.execute(f"select receipt_no from manage_receipt_no where year={yearid} and dept_id={depid}")
                                    out = cur.fetchone()
                                    if out != None:
                                        cur.execute(f"update receipt  set receipt_no = {out[0]},doc_name = '{doc_name}', case_no ={case_no} ,token_no = {token_no},pay_method='{payment_method}',sub_total = {sub_total},discount={discount},grand_total = {grand_total} ,date='{date}',year={yearid},dept_id={depid} where id = {self.repid} ")
                                        cur.execute(f'update manage_receipt_no set receipt_no=receipt_no+1 where year={yearid} and dept_id = {depid}')
                                
                                cur.execute(f"select id from receipt_charge where receipt_id={self.repid}")
                                charge_id_lst= []
                                for i in cur.fetchall():
                                    charge_id_lst.append(i[0])
                            
                                cur.execute("select id from year where is_current_year=1")
                                out = cur.fetchone()
                                if out != None:
                                    yearid = out[0]
                                    if len(charge_id_lst) == len(tree_data_update_lst): #that means user only update charges 
                                        try:
                                            for id,val in zip(charge_id_lst,tree_data_update_lst):
                                                cur.execute(f"update receipt_charge set name='{val[0]}',rate = {val[1]},no_of_times = {val[2]},total = {val[3]},year={yearid} where id = {id}")
                                        except Exception as e:
                                            print(e)
                                            messagebox.showerror("!","Error while updating chages",parent=self.main)
                                            self.edit['state'] = 'disable'
                                            return
                                    elif len(charge_id_lst) < len(tree_data_update_lst): # that means user update previour charge and add some new charges to it
                                        try:
                                            j =0 
                                            for i in charge_id_lst:
                                                cur.execute(f"update receipt_charge set name='{tree_data_update_lst[j][0]}',rate = {tree_data_update_lst[j][1]},no_of_times = {tree_data_update_lst[j][2]},total = {tree_data_update_lst[j][3]},year={yearid} where id = {i} ")
                                                j+=1
                                            
                                            for k in range(j,len(tree_data_update_lst)):
                                                cur.execute(f" insert into receipt_charge(receipt_id,name,rate,no_of_times,total,year) values({self.repid},'{tree_data_update_lst[k][0]}',{tree_data_update_lst[k][1]},{tree_data_update_lst[k][2]},{tree_data_update_lst[k][3]},{yearid}) ")
                                        
                                        except Exception as e:
                                            print(e)
                                            self.edit['state']='normal'
                                            messagebox.showerror("!","Error while updating chages",parent=self.main)
                                            return 
                                            
                                    elif len(charge_id_lst) > len(tree_data_update_lst): # that means user delete charges 
                                        for i in charge_id_lst:
                                            cur.execute(f"delete from receipt_charge where id = {i}")
                                        
                                        for k in range(0,len(tree_data_update_lst)):
                                            cur.execute(f" insert into receipt_charge(receipt_id,name,rate,no_of_times,total,year) values({self.repid},'{tree_data_update_lst[k][0]}',{tree_data_update_lst[k][1]},{tree_data_update_lst[k][2]},{tree_data_update_lst[k][3]},{yearid}) ")
                                else: #cannot find year id
                                    messagebox.showerror("!","cannot find year",parent = self.main)
                                    self.edit['state'] = 'normal'
                                    return
                            else:
                                messagebox.showerror("!","Cannot find record in year master",parent=self.main)
                                self.edit['state']='normal'
                                return
                        
                            con.commit()
                            self.display_data()
                            self.clear()
                            self.edit['state']='normal'
                        else:
                            messagebox.showerror("Error","Something wrong",parent=self.main)
                            self.edit['state']='normal'
                            return 
                    except Exception as e:
                        print( e)
                        self.edit['state']='normal'
                else:
                    messagebox.showerror("!","Empty either patient name, patient address or doctor name ",parent=self.main)
                    self.edit['state']='normal'
                    return 
            else:
                self.edit['state']='normal'
    
    
    def print_receipt(self):
        temp = self.add_to_db(des=1) 
        if temp == -1:
            return
        self.print['state'] = 'disabled'

        try:
            date = self.date_var.get()
            date = datetime.datetime.strptime(date,'%d/%m/%Y')

            cur.execute("select * from year  order by id desc")
            start_year = ""
            end_year = ""
            out = cur.fetchall()
            if len(out)>0 :  
                for i in out:  
                    if date >= datetime.datetime.strptime(i[1],'%d/%m/%Y') and date <= datetime.datetime.strptime(i[2],'%d/%m/%Y'):
                        start_year = i[1][6:]
                        end_year = i[2][6:]
                        break
                folder_path = "./saved_receipt"
                cur.execute("select folderpath from path_for_saving_receipt order by id desc")
                out  = cur.fetchone()
                if out != None:
                    final_path = out[0]
                
                    if  (os.path.isdir(final_path)):
                        try:   
                            p=None
                            receipt_no = self.receipt_no_var.get()
                            if start_year !="" and end_year !="":
                                creation_dt = str(datetime.datetime.today()).replace("/","_").replace(" ","_").replace(":","_")
                                p  = canvas.Canvas(f'{final_path}/receipt_{start_year}_{end_year}_{receipt_no}_{creation_dt}.pdf',pagesize=landscape(A5))
                                final_file_path = final_path + f"/receipt_{start_year}_{end_year}_{receipt_no}_{creation_dt}.pdf" 
                            else:
                                messagebox.showerror('!',"can not find start year or end year",parent=self.main)
                                self.print['state'] = 'normal'
                                return   
                        except:
                            messagebox.showerror("!","can not find folderpath",parent=self.main)
                            self.print['state'] = 'normal'
                            return 
                    else:
                        messagebox.showerror("go to settings -> change path","Path for saving receipt is incorrent please change it",parent=self.main)
                        self.print['state'] = 'normal'
                        return
                else:
                    messagebox.showerror("can not find path for saving receipt","can not find folderpath",parent=self.main)
                    self.print['state'] = 'normal'
                    messagebox.showwarning("please go to settings -> change path","Please enter path for saving receipt go to settings -> change path",parent=self.main)
                    return
            else:
                messagebox.showerror("!","Can not find year",parent=self.main)
                self.print['state'] = 'normal'
                return

        except Exception as e:
            print(e)
            messagebox.showerror("!","Can not find year in year master",parent=self.main)
            self.print['state'] = 'normal'
            return 

        try:
            patient_name = self.name_var.get()
        except:
            
            messagebox.showerror("!","Error while fetching patient name",parent=self.main)
            self.print['state'] = 'normal'
            return
    
        try:
            dep_name = str(self.department_name_var.get()).replace("'","").replace('"','').strip()
        except:
            
            messagebox.showerror("!","Error while fetching department name",parent=self.main)
            self.print['state'] = 'normal'
            return
        
        try:
            doc_name = str(self.doctor_name_var.get()).replace("'","").replace('"','').strip()
        except:
            messagebox.showerror("!","Error while fetching doctor name",parent=self.main)
            self.print['state'] = 'normal'
            return
    
        try:
            receipt_no = str(self.receipt_no_var.get())
        except:
            messagebox.showerror("!","Error while fetching receipt no",parent=self.main)
            self.print['state'] = 'normal'
            return

        try:
            date = str(self.date_var.get())
        except:
            messagebox.showerror("!","Error while fetching date",parent=self.main)
            self.print['state'] = 'normal'
            return
    
        try:
            case_no = str(self.case_no_var.get())
        except:
            messagebox.showerror("!","Error while fetching case no",parent=self.main)
            self.print['state'] = 'normal'
            return
            
        try:
            token_no = str(self.token_no_var.get())
        except:
            messagebox.showerror("!","Error while fetching token no",parent=self.main)
            self.print['state'] = 'normal'
            return

        try:
            pay_method  = str(self.payment_var.get())
        except:
            messagebox.showerror("!","Error while fetching payment method",parent=self.main)
            self.print['state'] = 'normal'
            return
            
        try:
            charge_data = []
            for i in self.tree.get_children():
                charge_data.append(self.tree.item(i,'values'))
        except:
            messagebox.showerror("!","Error while fetching charge data from",parent=self.main)
            self.print['state'] = 'normal'
            return
        
        try:
            grand_total = str(self.total_var.get())
        except:
            messagebox.showerror("!","Error while fetching grand total",parent=self.main)
            self.print['state'] = 'normal'
            return
       
        try:
            cur.execute('select receipt_banner from image order by id desc')
            out = cur.fetchone()
        
            if out != None:
                p.drawImage(f"{out[0]}",2,300,width=590,height=140) # this will come from banner 
                
            else:
                raise Exception("No path found")
        except Exception as e:
            print(e)
            messagebox.showwarning("!","Error while loading banner in receipt make sure your enterd correct path for banner",parent=self.main)
            self.print['state'] = 'normal'
            return

        if dep_name != "" and doc_name != "" and date != "" and case_no !="" and token_no !="" and patient_name != "" and pay_method != "":

            try:  
                # p.setPageSize(landscape((400,700))) #12.20
                # p.setPageSize(landscape((400,600))) #12.31
                # p.setPageSize((794,530)) # 12.12
                p.line(5,418,600,418)
                p.line(5,315,600,315)
                p.setFontSize(14)
                p.drawString(200,300,"PAYMENT RECEIPT")
                p.line(200,295,330,295)

                p.setFontSize(12)
                p.drawString(10,280,"Treatment Department : ")
                p.drawString(200,280,dep_name)

                p.drawString(10,260,"Name of Doctor : ")
                p.drawString(200,260,doc_name)

                
                p.drawString(380,280,"Receipt No :- ")
                p.drawString(480,280,f"{start_year}/{end_year}/{receipt_no}")

                p.drawString(380,260,"Date :- ")
                p.drawString(480,260,date)

                p.line(5,240,600,240) 

                p.drawString(10,225,"Case No :- ")
                p.drawString(100,225,case_no)

                p.drawString(380,230,"Token No :- ")
                p.drawString(480,230,token_no)

                
                p.drawString(10,210,"Received  with Thanks from Mr./Mrs.")
                p.drawString(210,210,patient_name)

                p.drawString(410,210,"for following by ")
                p.drawString(500,210,pay_method)
                p.line(210,200,400,200)
                p.line(500,200,590,200)

                p.line(5,195,600,195) #w 600

                p.drawString(40,180,"Description")
                p.line(40,175,100,175)
                p.drawString(500,180,"Amount")
                p.line(500,175,550,175)

                y = 160
                for i in charge_data:
                    p.drawString(40,y,i[0])
                    p.drawString(500,y,str(i[3]))
                    y-=25

                p.line(5,50,789,50)

                p.drawString(400,35,"Grand Total :-")
                p.drawString(500,35,str(grand_total))
                p.line(5,30,789,30)


                p.setFontSize(10)
                p.drawString(10,20,"Subject to Payment Realization")
                p.drawString(370,5,"For , Sardar Patel Seva Samaj Trust , Rajkot ")

                p.line(5,0,5,580)
                p.line(594,0,594,580)

                p.line(0,0,600,0)

                try:
                    p.save()
                    messagebox.showinfo("Success","Receipt Saved Succesfully",parent=self.main)
                except Exception as e:
                    print(e)
                    messagebox.showerror("error","Error while saving receipt",parent=self.main)
                    self.print['state'] = "enable"
                    return
                # try:
                #     win32api.ShellExecute(0, "print",f'{final_file_path}', None, ".", 0)
                # except Exception as e:
                #     print(e)
                #     messagebox.showerror("Error","Error while printing receipt.",parent=self.main)
                #     self.print['state'] = 'normal'
                
                try:
                    currentprinter = win32print.GetDefaultPrinter()
                except:
                    messagebox.showerror("!","Can not find printer",parent=self.main)
                    return
                
                try:
                    cwd = os.getcwd()
                    command = f'cmd /c {cwd}\PDFtoPrinter.exe "{final_file_path}" "{currentprinter}"'
                    os.system(command)
                    messagebox.showinfo("Success","Receipt Printed Successfully",parent=self.main)
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error in printing ","can not able to print receipt",parent=self.main)
                    return
                    
                self.print['state'] = 'normal'
                self.clear()
            except Exception as e:
                print(e)
                messagebox.showerror("!","cannot able to create receipt",parent=self.main)
                self.print['state'] = 'normal'
                return
        else:
            messagebox.showerror("!","Empty Fields",parent=self.main)
            self.print['state'] = 'normal'
            return

    def exit_f(self,e=None):
        res = messagebox.askquestion("?","are you sure you want to exit ?",parent=self.main)
        if res == "yes":
            self.main.destroy()
    
    def ctrl_p(self,e):
        self.print_receipt()
    
    def set_tree_focus(self,e):
        child = self.tree.get_children()
        self.tree.focus_force()
        if child:
            self.tree.focus(child[0])
            self.tree.selection_set(child[0])
    
    
    def change_to_address(self,e):
        self.address_entry.focus()
        self.address_entry.icursor('end')
    
    def change_to_age(self,e):
        self.age_entry.focus()  
        self.age_entry.icursor('end')

    def change_to_case_no(self,e):
        self.case_no_entry.focus()
        self.case_no_entry.icursor('end')

    def change_to_doc_nm(self,e):
        self.doctor_name_entry.focus()
        self.doctor_name_entry.icursor('end')
    
    def change_to_dept(self,e):
        self.department_name.focus()
    
    def change_to_date(self,e):
        self.date_entry.focus()
        self.date_entry.icursor('end')

    def select_male(self,e):
        self.gender_var.set(1)    
    
    def select_female(self,e):
        self.gender_var.set(2)    

    def update_record_call(self,e):
        if self.edit['state'] =='normal':
            self.update_record()
        else:
            messagebox.showerror("!","Please select receipt first",parent=self.main)
            return
    
    def focus_first(self,e):
        self.name_entry.focus()
    
   