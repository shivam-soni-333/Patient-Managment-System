import cmath
from email import message
from faulthandler import disable
from multiprocessing import parent_process
from random import randrange
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from case_entry import case_entry
from db_con import con,cur
import datetime
from reportlab.pdfgen import canvas
import os.path
import os
import win32api
import win32print
 
class all_receipt(Toplevel):
    yearid =-1
    def __init__(self,master=None):
        super().__init__(master=master)
        self.main =self
        
        self.main.resizable(False,False)


        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            

        self.main.title="All Receipt"
        window_height = 450
        window_width = 700
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()-30 # - 30 for proper setting up screen on main window

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.main.focus_force()
        self.main.update()

        
        #start_date 
        
        Label(self.main,text="Start Date :- ").place(x=10,y=5)
        self.start_date_var = StringVar()
        self.start_date_entry = Entry(self.main,width=35,textvariable=self.start_date_var)
        self.start_date_entry.focus()
        self.start_date_entry.place(x=80,y=0)
        self.start_date_var.set("D/M/Y")
        self.start_date_entry.bind("<FocusIn>",self.clean_entry)


        #end_date
        self.end_date_var = StringVar()
        Label(self.main,text="End Date :- ").place(x=350,y=5)
        self.end_date_entry = Entry(self.main,width=35,textvariable=self.end_date_var)
        self.end_date_entry.place(x=430,y=0)
        self.end_date_var.set("D/M/Y")
        self.end_date_entry.bind("<FocusIn>",self.clean_entry)
        #search button
        self.search = Button(self.main,text="Search",width=10,command=self.search)
        self.search.place(x=290,y=45)

        #treeview
        col = ['receipt_no','date','patient_name','doc_name','dep_name','pay_method','grand_total']
        self.tree = Treeview(self.main,column = col,show='headings')
        
        #setting up text
        self.tree.heading('receipt_no',text="Receipt No.")
        self.tree.heading('date',text='Date')
        self.tree.heading('patient_name',text="Patient Name")
        self.tree.heading('doc_name',text="Doctor Name")
        self.tree.heading('dep_name',text="Department Name")
        self.tree.heading('pay_method',text="Payment Method")
        self.tree.heading('grand_total',text="Grand Total")
    

        #setting up width
        self.tree.column(0,width=70)
        self.tree.column(1,width=100)
        self.tree.column(2,width=100)
        self.tree.column(3,width=100)
        self.tree.column(4,width=80)
        self.tree.column(5,width=80)
        self.tree.column(6,width=105)

        self.scrollbar = Scrollbar(self.main, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=680,y=80,height=299)

        self.tree.place(x=10,y=80,height=300)

        self.print = Button(self.main,text="Print",width=20,command=self.print_f)
        self.print.place(x=280,y=400,height=40)
        self.print['state'] = 'disable'
        
        Label(self.main,text=f"Total :- ").place(x=480,y=380)
        
        self.total_var  = DoubleVar()
        self.total_entry = Entry(self.main,width=15,textvariable=self.total_var)
        self.total_entry.place(x=530,y=380)

        self.clear = Button(self.main,text="Clear",width=15,command=self.clear_f)
        self.clear.place(x=560,y=415)

        self.clear['state'] = 'disable'
        self.display_data()
        self.set_current_year()

        self.calculate_total()

        #bind
        self.tree.bind("<<TreeviewSelect>>",self.get_selection)
        self.main.bind("<Control-p>",self.ctrl_p)
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        self.main.mainloop()
    
    def set_current_year(self):
        cur.execute("select * from year order by id desc limit 1")
        out = cur.fetchone()
        if out != None:
           self.start_date_var.set(out[1])
           self.end_date_var.set(out[2])

    def search(self):
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
   
        try:
            start_date_obj = datetime.datetime.strptime(start_date,'%d/%m/%Y')
            end_date_obj = datetime.datetime.strptime(end_date,'%d/%m/%Y')
            # if not int(end_date[6:]) >= int(start_date[6:]) :
            #     raise Exception
        except:
            messagebox.showerror("Error","Invalid date",parent=self.main)
            return
        
        cur.execute(f"select  receipt_no,date,pid,doc_name,dept_id,pay_method,grand_total from receipt")
        lst = cur.fetchall()
        receipt_lst = []
        if(len(lst) > 0):
            for i in lst: #lst is receipt list from database
                date = i[1]
                try:
                    date_obj = datetime.datetime.strptime(date,'%d/%m/%Y')
                except:
                    continue 
                if date_obj >=start_date_obj and date_obj<=end_date_obj:
                    receipt_lst.append(i)
            self.tree.delete(*self.tree.get_children()) 
            for i in receipt_lst:
                cur.execute(f"select name from patient where id={i[2]}")
                patient = cur.fetchone()
                cur.execute(f"select name from department where id ={i[4]}")
                department = cur.fetchone()
                if patient != None and department != None:
                    department  =department[0]
                    patient_name  = patient[0]
                    self.tree.insert('','end',values=(i[0],i[1],patient_name,i[3],department,i[5],i[6]))           
                else:
                    messagebox.showerror("!","can not find patient or department name",parent=self.main)
                    return
            self.calculate_total()
            self.main.update()
            self.print['state'] = 'disable'
            self.clear['state'] = 'disable'
            if len(self.tree.get_children()) == 0:
                messagebox.showinfo("No record found","there is not record between specified date range",parent=self.main)
            else:
                messagebox.showinfo("!","Found",parent=self.main)
        else:
            pass
    
    def print_f(self):
        if self.receipt_no != -1 and self.date != "":
            cur.execute(f"select id from receipt where receipt_no = {self.receipt_no} and date='{self.date}' ")
            out = cur.fetchone()
            if out != None:
                receipt_id = out[0]
                cur.execute(f"select name,total from receipt_charge where receipt_id = {receipt_id} ") 

                charge = cur.fetchall()
                if len(charge) > 0:
                    if (int(self.date[3:5]) >= 4):
                        start_year = self.date[6:]
                        end_year = int(start_year) + 1
                    else:
                        end_year = self.date[6:]
                        start_year = int(end_year)-1

                    
                    folder_path = "./saved_receipt"
                    cur.execute("select folderpath from path_for_saving_receipt order by id desc")
                    out  = cur.fetchone()
                    if out != None:
                    
                        final_path = out[0]
                        receipt_no = self.receipt_no
                        if start_year !="" and end_year !="":
                            creation_dt = str(datetime.datetime.today()).replace("/","_").replace(" ","_").replace(":","_")
                            p  = canvas.Canvas(f'{final_path}/receipt_{start_year}_{end_year}_{receipt_no}_{creation_dt}.pdf')
                            final_file_path = final_path + f"/receipt_{start_year}_{end_year}_{receipt_no}_{creation_dt}.pdf" 
                        else:
                            messagebox.showerror('!',"can not find start year or end year",parent=self.main)
                            self.print['state'] = 'normal'
                            return
                    
                try:
                    cur.execute('select receipt_banner from image order by id desc')
                    out = cur.fetchone()
                    if out != None:
                        p.drawImage(f"{out[0]}",5,375,width=784,height=170) # this will come from banner table
                    else:
                        raise Exception
                except Exception as e:
                    messagebox.showwarning("!","Error while loading banner in receipt make sure your enterd correct path for banner",parent=self.main)
                    
                

                try: 
                    p.setPageSize((794,530))

                    # p.line(5,500,789,500) # ---------

                    p.line(5,400,789,400)
                    p.setFontSize(20)
                    p.drawString(300,382,"PAYMENT RECEIPT")
                    p.line(300,377,492,377)

                    p.setFontSize(15)
                    p.drawString(10,350,"Treatment Department : ")
                    p.drawString(200,350,self.dept_name)

                    p.drawString(10,320,"Name of Doctor : ")
                    p.drawString(200,320,self.doc_name)

                    p.drawString(580,350,"Receipt No :- ")
                    p.drawString(680,350,f"{start_year}/{end_year}/{receipt_no}")

                    p.drawString(650,320,"Date :- ")
                    p.drawString(700,320,self.date)

                    p.line(5,300,789,300)

                    p.drawString(20,280,"Case No :- ")
                    p.drawString(100,280,self.case_no)

                    p.drawString(650,280,"Token No :- ")
                    p.drawString(740,280,self.token_no)

                    p.drawString(10,250,"Received  with  Thanks  from  Mr. / Mrs. ")
                    p.drawString(300,250,self.name)

                    p.drawString(600,250,"for following by ")
                    p.drawString(710,250,self.pay_method)
                    p.line(300,240,600,240)
                    p.line(710,240,780,240)

                    p.line(5,220,789,220)

                    p.drawString(40,200,"Description")
                    p.line(40,195,115,195)
                    p.drawString(700,200,"Amount")
                    p.line(700,195,750,195)

                    try:
                        cur.execute(f'select name ,total from receipt_charge where receipt_id = {self.receipt_id}')
                        charge_data = cur.fetchall()
                    except Exception as e:
                        print(e)
                        messagebox.showerror("!","can not able to fetch charges",parent=self.main)
                        self.print['state'] = 'normal'
                        return

                    y = 180
                    for i in charge_data:
                        p.drawString(40,y,i[0])
                        p.drawString(700,y,str(i[1]))
                        y-=25

                    p.line(5,50,789,50)

                    p.drawString(600,35,"Grand Total :-")
                    p.drawString(710,35,self.grand_total)
                    p.line(5,30,789,30)

                    p.setFontSize(10)
                    p.drawString(10,20,"Subject to Payment Realization")
                    p.drawString(550,5,"For , Sardar Patel Seva Samaj Trust , Rajkot ")

                    p.line(5,0,5,580)
                    p.line(789,0,789,580)

                    p.line(0,0,794,0)
                    try:
                        p.save()
                        messagebox.showinfo("Success","Receipt Saved Succesfully",parent=self.main)
                    except Exception as e:
                        print(e)
                        messagebox.showerror("error","Error while saving receipt",parent=self.main)
                        self.print['state'] = "normal"
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
                        self.print['state'] = 'normal'
                        return
                    
                    try:
                        cwd = os.getcwd()
                        command = f'{cwd}\PDFtoPrinter.exe "{final_file_path}" "{currentprinter}"'
                        os.system(command)
                        messagebox.showinfo("Success","Receipt Printed Successfully",parent=self.main)
                    except Exception as e:
                        print(e)
                        self.print['state'] = 'normal'
                        messagebox.showerror("Error in printing ","can not able to print receipt",parent=self.main)
                        return
                    
                        
                    self.print['state'] = 'normal'
                    self.clear_f()
                except Exception as e:
                    print(e)
                    messagebox.showerror("!","cannot able to create receipt",parent=self.main)
                    self.print['state'] ='normal'
                    return
                                

    def display_data(self):
        self.tree.delete(*self.tree.get_children())    
        cur.execute("select receipt_no,date,pid,doc_name,dept_id,pay_method,grand_total from receipt")
        out = cur.fetchall()
       
        if len(out) > 0:
            for i in out: 
                if len(i) == 7:
                    receipt_no = i[0]
                    date = i[1]
                    pid = i[2]
                    doc_name = i[3]
                    try:
                        cur.execute(f"select name from department where id = {i[4]}")
                        out = cur.fetchone()
                        if out != None:
                            dep_name  = out[0]
                    except:
                        messagebox.showerror("!","Unable to load department name",parent=self.main)
                        return
                    
                    pay_method = i[5]
                    grand_total = i[6]
                    cur.execute(f"select name from patient where id={pid}")
                    patient = cur.fetchone()
                    if patient != None:
                        patient_name  = patient[0]
                    self.tree.insert('','end',values=(receipt_no,date,patient_name,doc_name,dep_name,pay_method,grand_total))      
                
        else:
            pass

    
    def get_selection(self,e):
        try:
            self.print['state'] = 'normal'
            self.clear['state'] = 'normal'
            self.main.update()
            for item in self.tree.selection():
                values = self.tree.item(item,'values')
            
            self.receipt_no = values[0]
            self.date = str(values[1])
            self.name = str(values[2])
            self.doc_name =str(values[3])
            self.dept_name = str(values[4])
            self.pay_method = str(values[5])
            self.grand_total = str(values[6])
            
            cur.execute(f"select id from receipt where receipt_no = {self.receipt_no} and date = '{self.date}'")
            o = cur.fetchone()
            if o != None:
                self.receipt_id = o[0]
        except:
            pass

        try:
            cur.execute(f"select case_no,token_no from receipt where receipt_no={self.receipt_no} and date='{self.date}'")
            out = cur.fetchone()
            if out != None:
                self.case_no = str(out[0])
                self.token_no= str(out[1])
        except Exception as e:
            print(e)
            messagebox.showerror("!","Error while fetching case no and token no",parent=self.main)
            self.print['state'] = 'normal'
            self.clear_f()
            return
       
        
    def clear_f(self):
        self.start_date_var.set("D/M/Y")
        self.end_date_var.set("D/M/Y")
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        self.main.update()
        self.print['state'] = 'disable'
        self.receipt_no = -1
        self.date= ""
        self.clear['state'] = 'disable'
        
    def ctrl_p(self,e):
        print(self.print['state'])
        if self.print['state'] == 'normal':
            self.print_f()
        else:
            messagebox.showerror("!","Please select receipt that you want to print",parent=self.main)
    
    def clean_entry(self,e):
        if str(self.start_date_var.get()) == "D/M/Y":
            self.start_date_var.set("")
        
        if str(self.end_date_var.get()) == "D/M/Y":
            self.end_date_var.set("")
    
    def calculate_total(self):
        try:
            total = 0
            for item in self.tree.get_children():
                total += float(self.tree.item(item)['values'][6])
            self.total_var.set(total)
        except:
            messagebox.showerror("!","Can not calculate total",parent=self.main)
            return