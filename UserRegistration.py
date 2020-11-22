from tkinter import *
from tkinter import messagebox
import ToolTipText
import DataBase

root = Tk()
root.title('User Registration')
root.state('zoomed')
root.iconbitmap("images/register.ico")
image1 = PhotoImage(file="images/loginbackground.png")
label_for_image = Label(root, image=image1)
label_for_image.pack()
root.resizable(False, False)
frameUserData = Frame(root, bd=4, relief='raise', width=780, height=328)
frameUserData.place(x=500, y=150)


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)


db = DataBase.UserData()


def display():
    for row in db.view():
        ListName.insert(END, row[1])
        ListGen.insert(END, row[2])
        ListDOB.insert(END, row[3])
        ListQua.insert(END, row[4])
        ListAddress.insert(END, row[5])
        ListState.insert(END, row[6])
        ListPin.insert(END, row[7])
        ListEMail.insert(END, row[8])


def Register(event=''):
    try:
        if len(Firstname.get()) < 3:
            messagebox.showinfo('Information', 'Name cannot be less than 3 characters.')
        elif Honor.get()=='Honor':
            messagebox.showinfo('Information','Select Honor.')
        elif UserType.get() == 'Select User Type':
            messagebox.showinfo('Information', 'Select User Type.')
        elif Date.get() == 'Date' or Month.get() == 'Month' or Year.get() == 'Year':
            messagebox.showinfo('Information', 'Select Date of birth.')
        elif Qualification.get() == '':
            messagebox.showinfo('Information', 'Enter qualification.')
        elif Address.get() == '':
            messagebox.showinfo('Information', 'Enter address.')
        elif State.get() == 'State':
            messagebox.showinfo('Information', 'Select State.')
        elif len(Pin.get()) != 6:
            messagebox.showinfo('Information', 'Pin can be exact of 6 digit only.')
        elif EMail.get() == '':
            messagebox.showinfo('Information', 'Enter correct E-Mail ID.')
        elif Password.get() == '' or Password.get() != ConfirmPass.get():
            messagebox.showinfo('Information', 'Password and Confirm password do not match.')
        else:
            db.insert(Honor.get()+' '+Firstname.get(), UserType.get(), Date.get() + '/' + Month.get() + '/' + Year.get(),
                      Qualification.get(), Address.get(), State.get(), Pin.get(), EMail.get(), Password.get())
            messagebox.showinfo('Information', 'User successfully registered')
            Reset()
    except Exception:
        messagebox.showinfo('Error', 'E-Mail ID already exists.')


def Reset(event=''):
    Honor.set('Honor')
    Firstname.set('')
    UserType.set('Select User Type')
    Date.set('Date')
    Month.set('Month')
    Year.set('Year')
    Qualification.set('')
    Address.set('')
    State.set('Select State')
    Pin.set('')
    EMail.set('')
    Password.set('')
    ConfirmPass.set('')


def onlynum(e):
    if e.isdigit():
        return True
    elif e == '':
        return True
    else:
        return False


def AddStock(event=''):
    root.destroy()
    try:
        import AddProduct
        a=AddProduct.Design()
    except Exception:
        pass

def DeleteStock(event=''):
    root.destroy()
    try:
        import DeleteProduct
        a=DeleteProduct.DeleteStockView()
    except Exception:
        pass

def UpdateStock(event=''):
    root.destroy()
    try:
        import UpdateProduct
        a=UpdateProduct.Design()
    except Exception:
        pass


def Design():
    global Firstname,Honor, txtFirstname, UserType, Userlis, Date, DateLis, Month, MonthLis, Year, YearLis, Qualification, txtQualification, Address, txtAddress, State, StateLis, Pin, txtPin, EMail, txtEMail, Password, txtPassword, ConfirmPass

    Label(root, text='User Registration', bg='#ebced0', font=('Verdana', 40, 'bold'), justify=CENTER).place(x=460, y=20)
    Firstname = StringVar()
    Label(root, text='Full Name', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=150)
    Honor=StringVar()
    Honorist=['Mr.','Mrs.','Miss']
    HLis=OptionMenu(root,Honor,*Honorist)
    HLis.place(x=250,y=160)
    Honor.set('Honor')
    txtFirstname = Entry(root, textvariable=Firstname, font=15,width=14)
    txtFirstname.place(x=330, y=160)

    UserType = StringVar()
    UTList = ['Admin', 'Staff']
    Label(root, text='User Type', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=200)
    UserLis = OptionMenu(root, UserType, *UTList)
    UserLis.place(x=250, y=200)
    UserType.set('Select User Type')
    UserLis.configure(width=15)

    Date = StringVar()
    Month = StringVar()
    Year = StringVar()
    DateList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    MonthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    YearList = ['2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990',
                '1989', '1988', '1987', '1986', '1985']
    Label(root, text='Date of Birth', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=250)
    DateLis = OptionMenu(root, Date, *DateList)
    DateLis.place(x=250, y=250)
    Date.set('Date')
    MonthLis = OptionMenu(root, Month, *MonthList)
    MonthLis.place(x=322, y=250)
    Month.set('Month')
    MonthLis.configure(width=4)
    YearLis = OptionMenu(root, Year, *YearList)
    YearLis.place(x=400, y=250)
    Year.set('Year')
    YearLis.configure(width=5)

    Qualification = StringVar()
    Label(root, text='Qualification', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=300)
    txtQualification = Entry(root, textvariable=Qualification, font=15)
    txtQualification.place(x=250, y=300)

    Address = StringVar()
    Label(root, text='Address', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=350)
    txtAddress = Entry(root, textvariable=Address, font=15)
    txtAddress.place(x=250, y=350)

    State = StringVar()
    StateList = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Guwahati', 'Assam', 'Bihar',
                 'Chandigarh', 'Chhattisgarh', 'Dadra & Nagar Haveli,Daman & Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana',
                 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
                 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
                 'West Bengal']
    Label(root, text='State', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=400)
    StateLis = OptionMenu(root, State, *StateList)
    State.set('Select State')
    StateLis.place(x=250, y=400)
    StateLis.configure(width=30)

    Pin = StringVar()
    CheckPin = root.register(onlynum)
    Label(root, text='Pin', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=450)
    txtPin = Entry(root, textvariable=Pin, font=15)
    txtPin.place(x=250, y=450)
    txtPin.configure(validate='key', validatecommand=(CheckPin, '%P'))

    EMail = StringVar()
    Label(root, text='E-Mail ID', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=510)
    txtEMail = Entry(root, textvariable=EMail, font=15)
    txtEMail.place(x=250, y=510)

    Password = StringVar()
    Label(root, text='Password', bg='#ebced0', font=('Verdana', 15)).place(x=100, y=550)
    txtPassword = Entry(root, textvariable=Password, font=15, show='*')
    txtPassword.place(x=250, y=550)

    ConfirmPass = StringVar()
    Label(root, text='Confirm \n Password', bg='#ebced0', font=('Verdana', 15), justify=LEFT, anchor=N).place(x=100,
                                                                                                              y=600)
    Entry(root, textvariable=ConfirmPass, font=15, show='*').place(x=250, y=600)


Design()
RegisterButtonPhoto = PhotoImage(file=r"images/register.png")
RegBtn = Button(root, text='Register', image=RegisterButtonPhoto, command=Register)
RegBtn.place(x=500, y=510)
RegBtnTTP = ToolTipText.CreateToolTip(RegBtn, 'Register User')
root.bind('<Return>',Register)

ResetButtonPhoto = PhotoImage(file=r"images/reset.png")
ResBtn = Button(root, text='Reset', image=ResetButtonPhoto, command=Reset)
ResBtn.place(x=600, y=510)
ResBtnTTP = ToolTipText.CreateToolTip(ResBtn, 'Reset Form')
root.bind('<F5>',Reset)

AddStockButtonPhoto = PhotoImage(file=r"images/addstock.png")
AddBtn = Button(root, text='Add Stock', image=AddStockButtonPhoto, command=AddStock)
AddBtn.place(x=700, y=510)
AddBtnTTP = ToolTipText.CreateToolTip(AddBtn, 'Go to Add Product Menu from here.')
root.bind('<Control-A>', AddStock)
root.bind('<Control-a>', AddStock)

UpdateStockButtonPhoto = PhotoImage(file=r"images/updatestock.png")
UpdtBtn = Button(root, text='Update Stock', image=UpdateStockButtonPhoto, command=UpdateStock)
UpdtBtn.place(x=800, y=510)
UpdtBtnTTP = ToolTipText.CreateToolTip(UpdtBtn, 'Go to Update Stock Menu from here.')
root.bind('<Control-U>', UpdateStock)
root.bind('<Control-u>', UpdateStock)

DeleteStockButtonPhoto = PhotoImage(file=r"images/deletestock.png")
DltBtn = Button(root, text='Delete Stock', image=DeleteStockButtonPhoto, command=DeleteStock)
DltBtn.place(x=900, y=510)
DltBtnTTP = ToolTipText.CreateToolTip(DltBtn, 'Go to Delete Product Menu from here.')
root.bind('<Control-D>', UpdateStock)
root.bind('<Control-d>', UpdateStock)

scroll = Scrollbar(frameUserData)
scroll.grid(row=1, column=8, sticky='ns')
Label(frameUserData, text='Full Name').grid(row=0, column=0)
ListName = Listbox(frameUserData, width=17, height=20, yscrollcommand=scroll.set)
ListName.grid(row=1, column=0)
Label(frameUserData, text='User Type').grid(row=0, column=1)
ListGen = Listbox(frameUserData, width=9, height=20, yscrollcommand=scroll.set)
ListGen.grid(row=1, column=1)
Label(frameUserData, text='Date of Birth').grid(row=0, column=2)
ListDOB = Listbox(frameUserData, width=13, height=20, yscrollcommand=scroll.set)
ListDOB.grid(row=1, column=2)
Label(frameUserData, text='Qualification').grid(row=0, column=3)
ListQua = Listbox(frameUserData, width=15, height=20, yscrollcommand=scroll.set)
ListQua.grid(row=1, column=3)
Label(frameUserData, text='Address').grid(row=0, column=4)
ListAddress = Listbox(frameUserData, width=30, height=20, yscrollcommand=scroll.set)
ListAddress.grid(row=1, column=4)
Label(frameUserData, text='State').grid(row=0, column=5)
ListState = Listbox(frameUserData, width=15, height=20, yscrollcommand=scroll.set)
ListState.grid(row=1, column=5)
Label(frameUserData, text='Pin').grid(row=0, column=6)
ListPin = Listbox(frameUserData, width=7, height=20, yscrollcommand=scroll.set)
ListPin.grid(row=1, column=6)
Label(frameUserData, text='E-Mail').grid(row=0, column=7)
ListEMail = Listbox(frameUserData, width=25, height=20, yscrollcommand=scroll.set)
ListEMail.grid(row=1, column=7)

display()
root.mainloop()
