from cgitb import text
from email import message
from multiprocessing import parent_process
from tkinter import *
from tkinter import messagebox
from tracemalloc import start
from db_con import con,cur
import datetime 
from tkinter.ttk import *
class year_master(Toplevel):
    des = 0 
    def __init__(self,master=None):
        super().__init__(master=master)
        self.main = self
        self.main.title("Year Master")
        self.main.resizable(False,False)
        
        try:
            p1  = PhotoImage(file = './images/logo.png')
            self.main.iconphoto(False,p1)
        except Exception as e:
            messagebox.showerror("Error","Could not find logo file")
            


        window_height = 550
        window_width = 350

        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x_cordinate = int((screen_width/2)-(window_width/2))
        y_cordinate = int((screen_height/2)-(window_height/2))

        self.main.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        
        Label(self.main,text="Current Year ").place(x=10,y=0)
        self.start_date_lbl  = Label(self.main,text="")
        self.start_date_lbl.place(x=100,y=0)

        self.end_date_lbl = Label(self.main,text="")
        self.end_date_lbl.place(x=180,y=0)

        self.update_current_year()
        Label(self.main,text="-"*100).place(x=0,y=20)

        #start_date 
        
        Label(self.main,text="Start Date :- ").place(x=10,y=40)
        self.start_date_var = StringVar()
        self.start_date_entry = Entry(self.main,width=25,textvariable=self.start_date_var)
        self.start_date_entry.focus()
        self.start_date_entry.place(x=100,y=40,height=30)
    

        #end_date
        self.end_date_var = StringVar()
        Label(self.main,text="End Date :- ").place(x=10,y=80)
        self.end_date_entry = Entry(self.main,width=25,textvariable=self.end_date_var)
        self.end_date_entry.place(x=100,y=80,height=30)

        #submit button
        self.add = Button(self.main,text="Add",width=10,command=self.add_record)
        self.add.place(x=135,y=115)
        
        #set year to current year
        self.change_current_year = Button(self.main,text="set as current year",width=18,command=self.change_year)
        self.change_current_year.place(x=100,y=480)
        self.change_current_year['state'] = 'disable'

        #treeview
        col = ["yearid","start_date","end_date"]
        self.tree = Treeview(self.main,column=col,show='headings')
        
        self.tree.heading("yearid",text="YearId")
        self.tree.heading("start_date",text="Start Date")
        self.tree.heading("end_date",text="End Date")
        
        self.tree.column(0,width=40)
        self.tree.column(1,width=110)
        self.tree.column(2,width=131) 
        
       
        self.scrollbar = Scrollbar(self.main, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=332,y=150,height=299)


        self.tree.place(x=10,y=150,height=300)
        
        
        self.edit = Button(self.main,text="Edit",width=8,command=self.update_record)
        self.edit.place(x=10,y=480)
        self.edit['state'] = 'disable'

        # self.delete = Button(self.main,text="Delete",width=10,command=self.delete_record)
        # self.delete.place(x=110,y=460)
        # self.delete['state'] = 'disable'

        self.exit = Button(self.main,text="Exit",width=8,command=self.exit_f)
        self.exit.place(x=260,y=480)

        self.clear = Button(self.main,text="Clear",width=10,command = self.clear_f)

        self.main.focus_force()
        self.display_data()

        #shortcut label 
        Label(self.main,text="ctrl+e").place(x=25,y=520)
        Label(self.main,text="ctrl+s").place(x=135,y=520)
        Label(self.main,text="esc").place(x=280,y=520)


        #placeholder for entry
        self.start_date_entry.insert(0,'DD/MM/YYYY')
        self.end_date_entry.insert(0,'DD/MM/YYYY')
        

        #bind 

        self.main.bind("<Control-e>",self.ctrl_e)
        self.main.bind("<Control-s>",self.ctrl_s)
        self.main.bind("<Escape>",lambda e:self.main.destroy())
        self.start_date_entry.bind("<Button-1>", self.start_date_click)
        self.end_date_entry.bind("<Button-1>", self.end_date_click)

        self.tree.bind("<<TreeviewSelect>>",self.get_selection)
        self.main.mainloop()
    
    def display_data(self):
        try:
            cur.execute("select * from year")
            self.tree.delete(*self.tree.get_children())
            self.tree.tag_configure('current_year',background='#8af70c')
            
            cur_lst = cur.fetchall()
            
            for i in cur_lst:
                if i[3] == 0:
                    self.tree.insert("","end",values=(i[0],i[1],i[2]))
                elif i[3] == 1:
                    self.tree.insert('','end',values=(i[0],i[1],i[2]),tags=('current_year',))
            self.update_current_year()
        except:
            messagebox.showerror("!","Error while fetching year from database",parent=self.main)
            return
    
    def add_record(self):
        res = messagebox.askquestion("please verify it you can not delete this record!","Are you sure you want to add this year ?",parent=self.main)
        if res == "yes":
            if self.des == 0:
                self.add['state'] = 'disable'
                start_date=self.start_date_var.get().replace("'","").replace('"','').strip()
                end_date = self.end_date_var.get().replace("'","").replace('"','').strip()
                
                if start_date != "" and end_date != "" :
                    try:
                        start_date_obj = datetime.datetime.strptime(start_date,'%d/%m/%Y')
                        end_date_obj = datetime.datetime.strptime(end_date,'%d/%m/%Y')
                        
                        if start_date_obj < end_date_obj and  len(start_date) == 10 and len(end_date) == 10:
                            if(int(end_date[6:])-int(start_date[6:]) == 1 and int(end_date[6:]) <= int(datetime.datetime.today().strftime('%Y')) ):
                                print(start_date[3:5],end_date[3:5],start_date[0:2] , end_date[0:2])

                                if ( start_date[3:5] == "04" and end_date[3:5] == "03" and start_date[0:2] == "01" and end_date[0:2] == "31"):
                                    cur.execute(f"select * from year where start_date = '{start_date}' and end_date  = '{end_date}'")
                                    out = cur.fetchone()
                                    if out == None:
                                        cur.execute("update year set is_current_year =0")
                                        cur.execute(f"insert into year(start_date,end_date,is_current_year) values('{start_date}','{end_date}',1) ")
                                        cur.execute("select id from department")
                                        yearid = cur.lastrowid
                                        for id in cur.fetchall():
                                            cur.execute(f"insert into manage_receipt_no (receipt_no,year,dept_id) values(1,{yearid},{id[0]})")
                                        con.commit()
                                        messagebox.showinfo("Success","year added succesfully",parent=self.main)
                                        self.display_data()
                                        self.clear_f()
                                        self.add['state'] = 'normal'
                                    else:
                                        messagebox.showerror("!","This date is already present",parent=self.main)
                                        self.add['state'] = 'normal'
                                        return
                                else:
                                    raise Exception("day or moth invalid")
                            else:
                                raise Exception("year diff is not 1 or maybe entered future year ")
                        else:
                            raise Exception("invalid date")

                    except Exception as e:
                        print(e)
                        self.add['state'] = 'normal'
                        messagebox.showerror("!","invalid date",parent=self.main)
                else:
                    messagebox.showerror("Empty input!","invalid input",parent=self.main)
                    self.add['state'] = 'normal'
                    return
            
    def get_selection(self,e):
        self.edit['state'] = 'normal'
        self.change_current_year['state'] = 'normal'
        self.clear.place(x=135,y=115)
       
        self.des =1
        values = []
        for item in self.tree.selection():
            values = self.tree.item(item,'values')
        if len(values) == 3:
            self.yearid = values[0]
            start_date = values[1]
            end_date = values[2]
            
            self.start_date_var.set(start_date)
            self.end_date_var.set(end_date)
    
    def clear_f(self):

        self.start_date_var.set("")
        self.end_date_var.set("")
        self.start_date_entry.focus()
        for i in self.tree.selection():
            self.tree.selection_remove(i)
        
        self.main.update()
        self.edit['state'] = 'disable'
        self.change_current_year['state'] = 'disable'
      
      
        self.clear.place_forget()
        
        self.des = 0
        self.yearid = -1
    
    def update_record(self):
        if self.des == 1:
            self.edit['state'] = 'disable'
            start_date=self.start_date_var.get().replace("'","").replace('"','').strip()
            end_date = self.end_date_var.get().replace("'","").replace('"','').strip()
            
            try:
                if start_date !="" and end_date !="":
                    start_date_obj = datetime.datetime.strptime(start_date,'%d/%m/%Y')
                    end_date_obj = datetime.datetime.strptime(end_date,'%d/%m/%Y')
                    if start_date_obj < end_date_obj  and len(start_date) == 10 and len(end_date) == 10:
                        if(int(end_date[6:])-int(start_date[6:]) == 1 and int(end_date[6:]) <= int(datetime.datetime.today().strftime('%Y'))  ) :
                            cur.execute(f"update year set start_date = '{start_date}' , end_date = '{end_date}' where id = {self.yearid} ")
                            con.commit()
                            messagebox.showinfo("!","Year updated succesfully",parent=self.main)
                            self.clear_f()
                            self.display_data()
                        else:
                            raise Exception("Invalid date")
                    else:
                        raise Exception("Invalid date")
                else:
                    raise Exception
            except Exception as e:
                print(e)
                self.edit['state'] = 'normal'
                messagebox.showerror("!","invalid date",parent=self.main)
                return 
       
    
    def update_current_year(self): #update current year label 
        try:
            cur.execute("select * from year where is_current_year = 1")
            out = cur.fetchone()
            if out != None:
                self.start_date_lbl['text'] = out[1]
                self.end_date_lbl['text'] = out[2]
            else:
                raise Exception
        except:
            messagebox.showerror("!","Can not find current year in year master",parent=self.main)
            return
        
    def delete_record(self):
        
        res = messagebox.askquestion("?","Are you sure you want to delete this record ?",parent=self.main)
        if res == "yes":
            try:
                cur.execute(f"select is_current_year from year where id={self.yearid}")
                out = cur.fetchone()
                if out != None:
                    if out[0] == 1:
                        messagebox.showerror("you can not delete current year","Please change current year after changing try agin to delete this particular year",parent=self.main)
                      
                        return
                    else:
                        cur.execute(f"delete from year where id = {self.yearid} ")
                        con.commit()
                  
                    self.display_data()
                    self.clear_f()
            except:
                messagebox.showerror("!","can not able to delete year",parent=self.main)
                return
    
    def exit_f(self):
        self.main.destroy()
    
    def change_year(self):
        try:
            cur.execute("update year set is_current_year = 0")
            cur.execute(f"update year set is_current_year = 1 where id = {self.yearid}")
            con.commit()
            messagebox.showinfo("Success","current year changed",parent=self.main)
            self.display_data()
            self.update_current_year()
            self.clear_f()
        except Exception as e:
            print(e)
    
    def ctrl_e(self,e):
      
        if self.des ==1:
            self.update_record()
        else:
            messagebox.showerror("Unable to delete department","Please select record that you want to delete",parent=self.main)
       

    def ctrl_s(self,e):
        
        if self.des==1:
            self.change_year()
        else:
            messagebox.showerror("Unable to change current year","Please select year first",parent=self.main)

    def start_date_click(self,e):
        start_date = self.start_date_entry.get()
        if start_date == "DD/MM/YYYY":
            self.start_date_var = ""
    
    def end_date_click(self,e):
        end_date = self.end_date_entry.get()
        if end_date =="DD/MM/YYYY":
            self.end_date_var = ""
        