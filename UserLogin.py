from tkinter import *
from tkinter import messagebox
import ToolTipText
import DataBase

root = Tk()
root.state('zoomed')
root.resizable(False, False)
root.title('Login')
root.iconbitmap("images/login.ico")
image1 = PhotoImage(file="images/assorted-spices-near-white-ceramic-bowls-678414.png")
label_for_image = Label(root, image=image1)
label_for_image.pack()
UserName = Entry(root, width=40)
UserName.place(x=580, y=300)

Db = DataBase.UserData()


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)

Password = Entry(root, width=40)
Password.place(x=580, y=350)


def on_entry_click_name(event):
    if UserName.get() == 'Enter Username here:':
        UserName.delete(0, 'end')
        UserName.insert(0, '')
        UserName.config(fg='black')


def on_entry_click_pass(event):
    if Password.get() == 'Enter Password here:':
        Password.delete(0, 'end')
        Password.insert(0, '')
        Password.config(fg='black', show='*')


def on_focus_out_name(event):
    if UserName.get() == '':
        UserName.insert(0, 'Enter Username here:')
        UserName.config(fg='grey')


def on_focus_out_pass(event):
    if Password.get() == '':
        Password.insert(0, 'Enter Password here:')
        Password.config(fg='grey')


def login_chck(event=''):
    while True:
        Email = UserName.get()
        Pass = Password.get()
        result = Db.log(Email, Pass)
        if result:
            for i in result:
                messagebox.showinfo('Welcome ' + i[1], 'You are successfully logged in.')
                root.destroy()
                import AddProduct
                a = AddProduct.Design()
            break
        elif Email == 'admin' and Pass == 'admin':
            root.destroy()
            import BillingPage
            a = BillingPage.design()
            break
        else:
            messagebox.showerror('Error', 'Either Username or Password is incorrect.')
            break


UserName.insert(0, 'Enter Username here:')
UserName.bind('<FocusIn>', on_entry_click_name)
UserName.bind('<FocusOut>', on_focus_out_name)
UserName.config(fg='grey')
Password.insert(0, 'Enter Password here:')
Password.bind('<FocusIn>', on_entry_click_pass)
Password.bind('<FocusOut>', on_focus_out_pass)
Password.config(fg='grey')

LoginButtonPhoto = PhotoImage(file=r"images/login.png")
LgnBtn = Button(root, text='Login', image=LoginButtonPhoto, command=login_chck)
LgnBtn.place(x=650, y=400)
LgnBtnTTp = ToolTipText.CreateToolTip(LgnBtn, 'Login')
root.bind('<Return>', login_chck)
root.mainloop()
