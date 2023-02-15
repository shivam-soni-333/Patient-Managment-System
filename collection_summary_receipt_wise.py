from os import curdir
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from db_con import con,cur
import datetime
from reportlab.pdfgen import canvas
import os 
import win32api
import win32print

class receipt_wise(Toplevel):
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
            
        window_height = 300
        window_width = 800
    
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.main.focus_force()
        self.update()


        #dropdown
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
    
        self.print_btn = Button(self.main,text="Print",width=20,command=self.print_f)
        self.print_btn.place(x=350,y=35,height=30)
       

        self.main.bind("<Control-p>",self.ctrl_p)
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        


    def search_f(self):
        pass

    def print_f(self):
        try:
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            dept_name = self.department_name_var.get()
            start_date_obj = datetime.datetime.strptime(start_date,'%d/%m/%Y')
            end_date_obj = datetime.datetime.strptime(end_date,'%d/%m/%Y')
            self.start_date = start_date
            self.end_date = end_date
            self.dept_name = dept_name
        except Exception as e:
            print(e)
            messagebox.showerror("!","Invalid date",parent=self.main)
            return

        if start_date_obj <= end_date_obj:
            if dept_name  == "ALL":
                cur.execute("select folderpath from path_for_saving_receipt ")
                out = cur.fetchone()
                if out != None:
                    creation_dt = str(datetime.datetime.today().strftime("%d/%m/%Y")).replace("/","_")
                    p = canvas.Canvas(f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf")
                    final_file_path = f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf"  
                
                    p.setFontSize(20)
                    p.drawString(150,730,"Sardar Patel Seva Samaj Trust , Rajkot")
                    p.setFontSize(14)
                    p.drawString(170,700,f"Collection summary From {self.start_date} to {self.end_date}")
                    p.drawImage("./images/l.png",0,650,width=150,height=150)
                                        
                    p.line(0,660,700,660)
                    p.drawString(10,645,"DepartmentName")
                    p.drawString(150,645,"PatientName")
                    p.drawString(250,645,"ReceiptNo")
                    p.drawString(350,645,"Date")
                    p.drawString(450,645,"Payment Method")
                    p.line(0,640,700,640)

                    data  = {}
                    total_dict = {}
                    try:
                        self.dep_name_lst.remove('ALL')
                    except:
                        pass
                   

                    for dept_id in self.dep_id_lst:
                        cur.execute(f"select receipt_no,pid,date,pay_method,grand_total from receipt where dept_id={dept_id}")
                        cash = 0
                        pos = 0
                        cheque = 0
                        total = 0
                        filter_receipt = []
                        for j in cur.fetchall():
                            try:
                                date = datetime.datetime.strptime(j[2],'%d/%m/%Y')
                            except:
                                messagebox.showerror("!","Invalid date in database",parent=self.main)
                                return
                            
                            if date >= start_date_obj and date<=end_date_obj:
                                if j[3] == "CASH":
                                    cash+=j[4]
                                elif j[3] == "POS":
                                    pos+=j[4]
                                elif j[3] == "CHEQUE":
                                    cheque+=j[4]
                                total+=j[4]
                                pid = j[1] #pid
                               
                                cur.execute(f"select name from patient where id = {pid}")
                                name = cur.fetchone()
                                if name != None:
                                    temp = []
                                    temp.append(self.dep_name_lst[self.dep_id_lst.index(dept_id)])
                                    temp.append(name[0])
                                    temp.append(j[0])
                                    temp.append(j[2])
                                    temp.append(j[3])
                                
                                    filter_receipt.append(temp)
                                else:
                                    messagebox.showerror("!","Unable to fetch patient name",parent=self.main)
                                    return
                                
                                if len(filter_receipt) == 0:
                                    messagebox.showinfo("!","No Data Found",parent=self.main)
                                    return
                               
                                data[self.dep_name_lst[self.dep_id_lst.index(dept_id)]] = filter_receipt
                                temp = []
                                temp.append(cash)
                                temp.append(cheque)
                                temp.append(pos)
                                temp.append(total)
                                total_dict[self.dep_name_lst[self.dep_id_lst.index(dept_id)]]=temp
                    


                    def draw(x,y,data,total): 
                        for item in data.values():
                            for i in item:
                                p.drawString(x,y,str(i[0]))
                                p.drawString(x+100,y,str(i[1]))
                                p.drawString(x+200,y,str(i[2]))
                                p.drawString(x+300,y,str(i[3]))
                                p.drawString(x+400,y,str(i[4]))

                                y -= 20
                                if y <= 20:
                                    p.showPage()
                                    y=800
                            
                            p.line(0,y,700,y)
                            y-=20
                            p.drawString(5,y,f"Dept = {i[0]} ")
                            p.drawString(145,y,f"Cash  = {str(total [i[0]][0])}")
                            p.drawString(280,y,f"Cheque ={str(total[i[0]][1])}")
                            p.drawString(390,y,f"POS = {str(total[i[0]][2])}")
                            p.drawString(470,y,f"Total = {str(total[i[0]][3])}")
                            y-=10
                            p.line(0,y,700,y)
                            y-=20
                        
               
                    x= 50
                    y= 620
                    
                    if len(data) ==  0:
                        messagebox.showinfo("!","No Data Found",parent=self.main)
                        return
                        
                    
                    
                    draw(x,y,data,total_dict)

                    try:
                        p.save()
                        messagebox.showinfo("Success","Report Saved Succesfully",parent=self.main)
                    except Exception as e:
                        print(e)
                        messagebox.showerror("!","Error while saving receipt",parent=self.main)
                        return

                    # try:
                    #     win32api.ShellExecute(0, "print",f'{final_file_path}', None, ".", 0)
                    # except Exception as e:
                    #     messagebox.showerror("Error","Error while printing receipt.",parent=self.main)
                    #     return
                        
                    try:
                        currentprinter = win32print.GetDefaultPrinter()
                    except:
                        messagebox.showerror("!","Can not find printer",parent=self.main)
                        return
                    
                    try:
                        cwd = os.getcwd()
                        command = f'{cwd}\PDFtoPrinter.exe "{final_file_path}" "{currentprinter}"'
                        os.system(command)
                        messagebox.showinfo("Success","Receipt Printed Successfully",parent=self.main)
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error in printing ","can not able to print receipt",parent=self.main)
                        return
                

            else:
                
                try:
                    self.dep_name_lst.remove('ALL')
                except:
                    pass
                try:
                    index = self.dep_name_lst.index(dept_name)
                    dept_id = self.dep_id_lst[index]
                except Exception as e:
                    
                    return
                cur.execute(f'select receipt_no,pid,date,pay_method,grand_total from receipt where dept_id={dept_id}')
                
                res  = list(cur.fetchall())
              
               

                cur.execute("select folderpath from path_for_saving_receipt ")
                out = cur.fetchone()
                if out != None:
                    creation_dt = str(datetime.datetime.today().strftime("%d/%m/%Y")).replace("/","_")
                    p = canvas.Canvas(f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf")
                    final_file_path = f"{out[0]}/report_{self.dept_name}_from_{self.start_date.replace('/','_')}_to_{self.end_date.replace('/','_')}_{creation_dt}.pdf"  
                
                    p.setFontSize(20)
                    p.drawString(150,730,"Sardar Patel Seva Samaj Trust , Rajkot")
                    p.setFontSize(14)
                    p.drawString(170,700,f"Collection summary From {self.start_date} to {self.end_date}")
                    p.drawImage("./images/l.png",0,650,width=150,height=150)
                                        
                    p.line(0,660,700,660)
                    p.drawString(10,645,"DepartmentName")
                    p.drawString(150,645,"PatientName")
                    p.drawString(250,645,"ReceiptNo")
                    p.drawString(350,645,"Date")
                    p.drawString(450,645,"Payment Method")
                    p.line(0,640,700,640)

                 
                cash = 0
                pos = 0
                cheque = 0
                total = 0
                filter_receipt = []

                for j in res:
                    try:
                        date = datetime.datetime.strptime(j[2],'%d/%m/%Y')
                    except:
                        messagebox.showerror("!","Invalid date",parent=self.main)
                        return
                    
                    if date >= start_date_obj and date<=end_date_obj:
                        if j[3] == "CASH":
                            cash+=j[4]
                        elif j[3] == "POS":
                            pos+=j[4]
                        elif j[3] == "CHEQUE":
                            cheque+=j[4]
                        total+=j[4]
                        pid = j[1] #pid
                        cur.execute(f"select name from patient where id = {pid}")
                        name = cur.fetchone()
                        if name != None:
                            temp = []
                            temp.append(dept_name)
                            temp.append(name[0])
                            temp.append(j[0])
                            temp.append(j[2])
                            temp.append(j[3])
                         
                            
                            filter_receipt.append(temp)
                        else:
                            messagebox.showerror("!","Unable to fetch patient name",parent=self.main)
                            return

                def draw(x,y,data): 
                    for item in data.values():
                        for i in item:
                            p.drawString(x,y,str(i[0]))
                            p.drawString(x+100,y,str(i[1]))
                            p.drawString(x+200,y,str(i[2]))
                            p.drawString(x+300,y,str(i[3]))
                            p.drawString(x+400,y,str(i[4]))

                            y -= 20
                            if y <= 20:
                                p.showPage()
                                y=800
                        
                        p.line(0,y,700,y)
                        y-=20
                        p.drawString(5,y,f"Department = {dept_name} ")
                        p.drawString(145,y,f"Cash  = {str(cash)}")
                        p.drawString(280,y,f"Cheque ={str(cheque)}")
                        p.drawString(390,y,f"POS = {str(pos)}")
                        p.drawString(470,y,f"Total = {str(total)}")
                        y-=10
                        p.line(0,y,700,y)
                        y-=20
                    
                        
                
                if len(filter_receipt) == 0:
                    messagebox.showinfo("!","No Data Found",parent=self.main)
                    return

                data  = {}
                data[dept_name] = filter_receipt
                if len(filter_receipt) >0:
                    draw(50,620,data)
                else:
                    messagebox.showerror("!","No Data Found",parent=self.main)
                    return
                    
                try:
                    p.save()
                    messagebox.showinfo("Success","Report Saved Succesfully",parent=self.main)
                except Exception as e:
                    print(e)
                    messagebox.showerror("!","Error while saving receipt",parent=self.main)
                    return

                # try:
                #     win32api.ShellExecute(0, "print",f'{final_file_path}', None, ".", 0)
                # except Exception as e:
                #     messagebox.showerror("Error","Error while printing receipt.",parent=self.main)
                #     return

                try:
                    currentprinter = win32print.GetDefaultPrinter()
                except:
                    messagebox.showerror("!","Can not find printer",parent=self.main)
                    return
                
                try:
                    cwd = os.getcwd()
                    command = f'{cwd}\PDFtoPrinter.exe "{final_file_path}" "{currentprinter}"'
                    os.system(command)
                    messagebox.showinfo("Success","Receipt Printed Successfully",parent=self.main)
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error in printing ","can not able to print receipt",parent=self.main)
                    return
                

                    

        else:
            messagebox.showerror("!","Invalid date",parent=self.main)
            return



    def ctrl_p(self,e):
        self.print_f()
