#department wise collection summary 
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from db_con import cur,con
import datetime
from reportlab.pdfgen import canvas
import os 
import win32api
import win32print

class collection_summary(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        
        self.main=self
        self.main.title("Collection Summary ")



        self.main.resizable(False,False)

        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            
        window_height = 700
        window_width = 800
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.main.focus_force()
        self.update()

        #drop
        Label(self.main,text="Department Name").place(x=10,y=5)
        self.department_name_var = StringVar()
        self.department_name = Combobox(self.main,textvariable = self.department_name_var,state='readonly',width=20)
       #this list will come from database
        self.department_name.place(x=130,y=0)
        self.department_name.bind("<Return>",lambda e:self.start_date_entry.focus())
        self.dep_name_lst = ['ALL']
        self.dep_id_lst = []
        try:
            cur.execute("select * from department")
            for i in cur.fetchall():
                self.dep_name_lst.append(i[1])
                self.dep_id_lst.append(i[0])
            self.department_name['values']  = self.dep_name_lst
            if len(self.dep_name_lst) > 0:
                self.department_name_var.set(self.dep_name_lst[0])
        except Exception as e:
            print(e)
            messagebox.showerror("!","Can not able to fetch department",parent=self.main)
    
        #startdate
        Label(self.main,text="Start Date :- ").place(x=325,y=5)
        self.start_date_var = StringVar()
        self.start_date_entry = Entry(self.main,width=20,textvariable=self.start_date_var)
        self.start_date_entry.focus()
        self.start_date_entry.place(x=400,y=0)
        self.start_date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
        self.start_date_entry.icursor(10)
        self.start_date_entry.bind("<Return>",lambda e:self.end_date_entry.focus())
        
        #end_date
        self.end_date_var = StringVar()
        Label(self.main,text="End Date :- ").place(x=570,y=5)
        self.end_date_entry = Entry(self.main,width=20,textvariable=self.end_date_var)
        self.end_date_entry.place(x=640,y=0)
        self.end_date_var.set(str(datetime.datetime.today().strftime('%d/%m/%Y')))
        self.end_date_entry.bind("<Return>",lambda e:self.search_f())

        #search button command= 
        self.search = Button(self.main,text="Search",width=10,command=self.search_f)
        self.search.place(x=370,y=35)

        col = ['department_name','cash','cheque','pos','receipt','total']
        self.tree= Treeview(self.main,columns=col,show='headings')
        
        self.tree.column(0,width=150)
        self.tree.column(1,width=100)
        self.tree.column(2,width=100)
        self.tree.column(3,width=150)
        self.tree.column(4,width=100)
        self.tree.column(5,width=100)

        self.tree.heading(0,text="Department Name")
        self.tree.heading(1,text="Cash")
        self.tree.heading(2,text="Cheque")
        self.tree.heading(3,text="POS")
        self.tree.heading(4,text="Receipt No. range")
        self.tree.heading(5,text="Total")

        self.tree.place(x=25,y=70,height=500)

      
        scrollbar = Scrollbar(self.main,orient=VERTICAL,command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=770,y=70,height=500)
    
        self.print_btn = Button(self.main,text="Print",width=20,command=self.print_f)
        self.print_btn.place(x=350,y=600,height=30)
        self.print_btn['state'] = 'disable'

        self.main.bind("<Control-p>",self.ctrl_p)
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        
        self.main.mainloop()

    def search_f(self):
        dept_name = self.department_name_var.get().replace("'","").replace('"','').strip()
        start_date = self.start_date_var.get().replace("'","").replace('"','').strip()
        end_date = self.end_date_var.get().replace("'","").replace('"','').strip()

        try:
            start_date_obj = datetime.datetime.strptime(start_date,'%d/%m/%Y')
            end_date_obj = datetime.datetime.strptime(end_date,'%d/%m/%Y')
            self.start_date = start_date
            self.end_date = end_date
            self.dept_name = dept_name
        except Exception as e:
            print(e)
            messagebox.showerror("!","Invalid date",parent=self.main)
            return
        self.data  = []

        if start_date_obj <= end_date_obj:
            if dept_name == "ALL": #all department 
                dept_lst = self.department_name['values']
                cur.execute("select id,name from department")
                self.tree.delete(*self.tree.get_children())
                self.grand_total = 0
                for deptid in cur.fetchall(): #deptid = (1,'general') in this format
                    cur.execute(f"select pay_method,grand_total,receipt_no,date from receipt where dept_id={deptid[0]}")
                    cash =0
                    pos = 0
                    cheque = 0 
                    total = 0
                    receipt_range = []
                    receipt = cur.fetchall()
                    for j in receipt:
                        try:
                            date = datetime.datetime.strptime(j[3],'%d/%m/%Y')
                        except:
                            messagebox.showerror("!","Invalid date",parent=self.main)
                            return
                        if date >= start_date_obj and date<=end_date_obj:
                            if j[0] == "CASH":
                                cash+=j[1]
                            elif j[0] == "POS":
                                pos+=j[1]
                            elif j[0] == "CHEQUE":
                                cheque+=j[1]
                            receipt_range.append(j[2])
                            total+=j[1]
                    
                    if(len(receipt_range) > 0):
                        self.tree.insert('','end',values=(deptid[1],str(cash),str(cheque),str(pos),str(str(receipt_range[0])+" to "+str(receipt_range[-1])),str(total)))
                        lst  = []
                        lst.append(deptid[1])
                        lst.append(str(cash))
                        lst.append(str(cheque))
                        lst.append(str(pos))
                        temp =  str(str(receipt_range[0])+" to "+str(receipt_range[-1]))
                        lst.append(temp)
                        self.grand_total+=total
                        lst.append(str(total))
                        self.data.append(lst)
                
                    
              
                
            else:
                self.tree.delete(*self.tree.get_children())
               
                dept_name = self.department_name_var.get()
                index = self.dep_name_lst.index(dept_name)
                dept_id = self.dep_id_lst[index-1]
                cur.execute(f"select pay_method,grand_total,receipt_no,date from receipt where dept_id={dept_id}")
                
                cash =0
                pos = 0
                cheque = 0 
                total = 0
                receipt_range = []
                
                for j in cur.fetchall():
                    try:
                        date = datetime.datetime.strptime(j[3],'%d/%m/%Y')
                    except:
                        messagebox.showerror("!","Invalid date",parent=self.main)
                        return
                    if date >= start_date_obj and date<=end_date_obj:
                        if j[0] == "CASH":
                            cash+=j[1]
                        elif j[0] == "POS":
                            pos+=j[1]
                        elif j[0] == "CHEQUE":
                            cheque+=j[1]
                        receipt_range.append(j[2])
                        total+=j[1]
                if len(receipt_range) > 0:
                    self.tree.insert('','end',values=(dept_name,str(cash),str(cheque),str(pos),str(str(receipt_range[0])+" to "+str(receipt_range[-1])),str(total)))
                    lst  = []
                    lst.append(dept_name)
                    lst.append(str(cash))
                    lst.append(str(cheque))
                    lst.append(str(pos))
                    temp =  str(str(receipt_range[0])+" to "+str(receipt_range[-1]))
                    lst.append(temp)
                    lst.append(str(total))
                    self.data.append(lst)
            
            self.print_btn['state'] ='normal'

        if len(self.tree.get_children()) == 0 :
            messagebox.showwarning("No data found","No Receipt was found during this date range",parent=self.main)
            self.print_btn['state'] = 'disable'

    def print_f(self):
   
        cur.execute("select folderpath from path_for_saving_receipt ")
        out = cur.fetchone()
        if out != None:
            creation_dt = str(datetime.datetime.today().strftime("%d/%m/%Y")).replace("/","_")

            if self.dept_name !="" and self.start_date != "" and self.end_date !="" and creation_dt != "":          
                p = canvas.Canvas(f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf")

                final_file_path = f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf"  
                p.setFontSize(20)
                p.drawString(150,730,"Sardar Patel Seva Samaj Trust , Rajkot")
                p.setFontSize(14)
                p.drawString(170,700,f"Collection summary From {self.start_date} to {self.end_date}")
                p.drawImage("./images/l.png",0,650,width=150,height=150)

                
                def draw(y):
                        p.line(0,y,700,y)
                        y-=20
                        p.drawString(10,y,"Department Name") #510 - 490 = 20
                        p.drawString(150,y,i[0]) 
                        y-=20
                        p.line(0,y,700,y) #490-475 = 15

                        y-=20
                        p.drawString(10,y,"CASH -->")
                        p.drawString(150,y,i[1])

                        y-=20
                        p.drawString(10,y,"CHEQUE -->")
                        p.drawString(150,y,i[2])

                        y-=20
                        p.drawString(10,y,"POS --> ")
                        p.drawString(150,y,i[3])

                        y-=20
                        p.drawString(10,y,"Receipt No. Range --> ")
                        p.drawString(150,y,i[4])

                        y-=20
                        p.line(0,y,700,y)
                        y-=20
                        p.drawString(10,y,"Total --> ")
                        p.drawString(150,y,i[5])
                        y-=20
                        p.line(0,y,700,y)
                        return y
                
                y = 660
               
                for i in self.data:
                    y = draw(y)
                    if  y <= 160:
                        p.showPage()
                        y=700
                
                p.drawString(10,y-40,"Total of all departments -->")
                p.drawString(200,y-40,str(self.grand_total)) 
                try:
                    p.save()
                    messagebox.showinfo("Success","Report Saved Succesfully",parent=self.main)
                except Exception as e:
                    print(e)
                    messagebox.showerror("!","Error while saving receipt",parent=self.main)


                # try:
                #     win32api.ShellExecute(0, "print",f'{final_file_path}', None, ".", 0)
                # except Exception as e:
                #     print(e)
                #     messagebox.showerror("Error","Error while printing receipt.",parent=self.main)
                #     self.print_btn['state'] = 'normal'
                #     return


                try:
                    currentprinter = win32print.GetDefaultPrinter()
                except:
                    messagebox.showerror("!","Can not find printer",parent=self.main)
                    self.print_btn['state'] = 'normal'
                    return
                
                try:
                    cwd = os.getcwd()
                    command = f'{cwd}\PDFtoPrinter.exe "{final_file_path}" "{currentprinter}"'
                    os.system(command)
                    messagebox.showinfo("Success","Receipt Printed Successfully",parent=self.main)
                except Exception as e:
                    print(e)
                    self.print_btn['state'] = 'normal'
                    messagebox.showerror("Error in printing ","can not able to print receipt",parent=self.main)
                    return
                

    def ctrl_p(self,e):
        print(self.print_btn['state'])
        if self.print_btn['state'] =='normal':
            self.print_f()
                  


