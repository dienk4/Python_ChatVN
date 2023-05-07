import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class ShowFOrm:
    def __init__(self, home):
        self.home = home

        self.show_label = Label(self.home, text="ShowForm", font=('Arial', 24), foreground="white", bg="#008080")
        self.show_label.pack(fill=X)

        self.label = Label(self.home, text='Search information:', font=('Arial', 10))
        self.label.place(x=15, y=84)

        self.entry = Entry(self.home, font=('Arial', 10),width=17)
        self.entry.place(x=140, y=84)

        self.scrollbar_y = Scrollbar(self.home)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)

        self.scrollbar_x = Scrollbar(self.home, orient=HORIZONTAL)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.list = ttk.Treeview(self.home,columns=("name", "user", "SDT","email","pass"),yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set,
                            height=23)

        # Cấu hình các cột
        self.list.column("#0", width=0, stretch=NO)
        self.list.column("name", anchor=W, width=110)
        self.list.column("user", anchor=W, width=70)
        self.list.column("SDT", anchor=W, width=70)
        self.list.column("email", anchor=W, width=110)
        self.list.column("pass", anchor=W, width=70)
        # Cấu hình tiêu đề các cột
        self.list.heading("#0", text="", anchor=W)
        self.list.heading("name", text="Name", anchor=CENTER)
        self.list.heading("user", text="User", anchor=CENTER)
        self.list.heading("SDT", text="SDT", anchor=CENTER)
        self.list.heading("email", text="Email", anchor=CENTER)
        self.list.heading("pass", text="Password", anchor=CENTER)

        self.list.place(x=0, y=116)

        self.scrollbar_y.config(command=self.list.yview)
        self.scrollbar_x.config(command=self.list.xview)

        self.show = Button(self.home, text='👀', command=self.show, font=('Arial', 15),borderwidth=0)
        self.show.place(x=350, y=72)

        self.clear = Button(self.home, text='🗑️', command=self.clear, font=('Arial', 15),borderwidth=0)
        self.clear.place(x=390, y=74)

        self.search= Button(self.home,text='🔍', font=('Arial', 15),foreground='#0066CC',borderwidth=0,command=self.search)
        self.search.place(x=265, y=75)

        self.fix = Button(self.home, text='🛠', command=self.fix, font=('Arial', 15),borderwidth=0)
        self.fix.place(x=310, y=74)

        self.excel = Button(self.home, text='👉Export excel', command=self.excel, font=('Arial', 11),fg='#009900',borderwidth=0)
        self.excel.place(x=330, y=50)

        self.bn_return = Button(self.home, text='←', font=('Arial', 18), borderwidth=0, fg='#003399',
                                command=self.return_main)
        self.bn_return.place(x=5, y=42)
    def excel(self):
        self.toplevel = Toplevel(self.home)
        self.toplevel.title('Export excel')
        self.toplevel.geometry("200x100+300+200")
        self.name_label = Label(self.toplevel,text='Name file:',font=('Arial', 15))
        self.name_label.pack()
        self.e_name = Entry(self.toplevel,font=('Arial', 15))
        self.e_name.pack()
        self.ok=Button(self.toplevel,text='🇴 🇰',font=('Arial', 15),background='#006699',foreground='white',command=self.ok)
        self.ok.pack()
    def ok(self):
        self.e = self.e_name.get()

        if self.e == '':
            messagebox.showinfo('Notification', 'Please enter information')
        else:
            conn = sqlite3.connect('Data\\dangky.db')
            df = pd.read_sql_query('SELECT * FROM dangky', conn)
            df.to_excel(f'{self.e}.xlsx', index=False)
            conn.close()
            self.toplevel.destroy()
    def fix(self):


        self.toplv = Toplevel(self.home)
        self.toplv.geometry('450x450+300+200')
        self.toplv.title('Fix information')

        self.register = Label(self.toplv, text="Change information", font=('Arial', 24), foreground="white", bg="#008080")
        self.register.pack(fill=X)

        self.name1 = Label(self.toplv, text="First and Last name:", font=('Arial', 14), fg='#2c3e50')
        self.name1.place(x=40, y=130)

        self.user1 = Label(self.toplv, text="User:", font=('Arial', 14), fg='#2c3e50')
        self.user1.place(x=40, y=170)

        self.SDT1 = Label(self.toplv, text="Phone number:", font=('Arial', 14), fg='#2c3e50')
        self.SDT1.place(x=40, y=210)

        self.email1 = Label(self.toplv, text="Email:", font=('Arial', 14), fg='#2c3e50')
        self.email1.place(x=40, y=250)

        self.password1 = Label(self.toplv, text="Password:", font=('Arial', 14), fg='#2c3e50')
        self.password1.place(x=40, y=290)

        # Entry
        self.name_entry = Entry(self.toplv, font=('Arial', 14))
        self.name_entry.place(x=220, y=130, width=200)

        self.user_entry = Entry(self.toplv, font=('Arial', 14))
        self.user_entry.place(x=220, y=170, width=200)

        self.SDT_entry = Entry(self.toplv, font=('Arial', 14))
        self.SDT_entry.place(x=220, y=210, width=200)

        self.email_entry = Entry(self.toplv, font=('Arial', 14))
        self.email_entry.place(x=220, y=250, width=200)

        self.password_entry = Entry(self.toplv, font=('Arial', 14))
        self.password_entry.place(x=220, y=290, width=200)

        self.bn_save = Button(self.toplv,text='Save',font=('Arial', 15),background='#2980b9',foreground='white',command=self.save)
        self.bn_save.place(x=200,y=330)

        selected_item = self.list.selection()
        if selected_item:
            user1 = self.list.item(selected_item)['values'][0]
            user2 = self.list.item(selected_item)['values'][1]
            user3 = self.list.item(selected_item)['values'][2]
            user4 = self.list.item(selected_item)['values'][3]
            user5 = self.list.item(selected_item)['values'][4]

            self.name_entry.insert(END, user1)
            self.user_entry.insert(END, user2)
            self.SDT_entry.insert(END, user3)
            self.email_entry.insert(END, user4)
            self.password_entry.insert(END, user5)
    def save(self):
        name = self.name_entry.get()
        user = self.user_entry.get()
        SDT=self.SDT_entry.get()
        email=self.email_entry.get()
        passw=self.password_entry.get()

        conn = sqlite3.connect('../Data/dangky.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE dangky SET name=?,SDT=?,email=?,pass=? WHERE user=?', (name,SDT,email,passw,user))
        conn.commit()
        conn.close()
        self.toplv.destroy()
    def search(self):
        e = self.entry.get()
        conn = sqlite3.connect('Data\\dangky.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dangky WHERE user =  "{}"'.format(e))

        row = cursor.fetchall()
        if row:
            self.list.delete(*self.list.get_children())
            for i in row:
                self.list.insert('', 'end', values=i)
        conn.close()
    def clear(self):
        selected_item = self.list.selection()
        if selected_item:
            user = self.list.item(selected_item)['values'][1]
            conn = sqlite3.connect('Data\\dangky.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dangky WHERE user = '{}'".format(user))
            conn.commit() # cập nhật giá trị

            self.list.delete(selected_item)


    def show(self):
        conn = sqlite3.connect('Data\\dangky.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dangky")
        rows = cursor.fetchall()
        self.list.delete(*self.list.get_children())
        for i in rows:
            self.list.insert('', 'end', values=i)
        conn.close()

    def return_main(self):
        self.show_label.destroy()
        self.list.destroy()
        self.bn_return.destroy()
        self.show.destroy()
        self.scrollbar_y.destroy()
        self.scrollbar_x.destroy()
        self.clear.destroy()
        self.entry.destroy()
        self.label.destroy()
        self.search.destroy()
        self.fix.destroy()
        self.excel.destroy()
        # a = main(self.home)
root = Tk()
root.geometry("460x620+420+60")
root.resizable(False, False)
root.title("Chat")

my_register = ShowFOrm(root)

root.mainloop()