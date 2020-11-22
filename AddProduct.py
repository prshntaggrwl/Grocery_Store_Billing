from tkinter import *
from tkinter import messagebox
import ToolTipText
import DataBase
import openpyxl
from datetime import datetime
import os

root = Tk()
root.title('Stock Maintenance')
root.state('zoomed')
root.resizable(False, False)
root.iconbitmap("images/addstock.ico")
image1 = PhotoImage(file='images/coconut-filled-with-slice-of-fruits-1030973.png')
label_for_image = Label(root, image=image1)
label_for_image.pack()


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)

frameStockData = Frame(root, bd=4, relief='raise')
frameStockData.place(x=500, y=150)

StockMaintain = DataBase.Stock()
ObjStockView = DataBase.AvailableStockView()

ObjStockView.view(frameStockData, ObjStockView.scroll_view, 20, ObjStockView.onmousewheel)
ObjStockView.display(StockMaintain)


def AddStock(event=''):
    a = ItemName.get().upper()[0:4]
    b = ItemType.get().upper()[0:4]
    c = Weight.get().upper()[0:1]
    ref = a + b + c
    #    try:
    if txtItemName.get() == '' or txtWeight.get() == '' or txtItemType.get() == '' or txtQuantity.get() == '' or txtMRP.get() == '':
        messagebox.showinfo('Information', 'Kindly fill all details.')
    else:
        StockMaintain.insert(Barcode.get(), ref, ItemName.get() + '(' + Weight.get() + ')', ItemType.get(),
                             Quantity.get(),
                             MRP.get(),
                             Expiry.get())
        messagebox.showinfo('Information',
                            'Product with Ref. No. ' + str(ref) + ' is successfully added.')
        ObjStockView.display(StockMaintain)
        clearvalues()


#    except Exception:
#        messagebox.showerror('Error', 'Product with same Reference Number ' + Barcode.get() + ' already exists!')


def Delete(event=''):
    root.destroy()
    try:
        import DeleteProduct
        a = DeleteProduct.DeleteStockView()
    except Exception:
        pass


def Update(event=''):
    root.destroy()
    try:
        import UpdateProduct
        a = UpdateProduct.Design()
    except Exception:
        pass


def Register(event=''):
    root.destroy()
    try:
        import UserRegistration
        a = UserRegistration.Design()
    except Exception:
        pass


def onlynum(e):
    if e.isdigit():
        return True
    elif e == '':
        return True
    else:
        return False


def saverep():
    a = StockMaintain.view()
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.title = 'Stock Details'
    now = datetime.now()
    dt_string = now.strftime('%d/%b/%Y %H:%M:%S')

    cols = (['Barcode', 'Item Reference', 'Item Name', 'Category', 'Stock', 'M.R.P.', 'Expiry'])
    sheet.append(cols)
    for i in a:
        sheet.append(i)

    if not os.path.exists('C:\\Reports'):
        os.makedirs('C:\\Reports')

    wb.save('C:\\Reports\\Stock Details Report.xlsx')


def clearvalues():
    txtBarcode.delete(0, END)
    txtItemName.delete(0, END)
    txtWeight.delete(0, END)
    txtQuantity.delete(0, END)
    txtMRP.delete(0, END)
    txtExpiry.delete(0, END)
    txtItemType.delete(0, END)


def Design():
    try:
        global Barcode, txtBarcode, ItemRef, ItemName, txtItemName, Weight, txtWeight, ItemType, txtItemType, Quantity, txtQuantity, MRP, txtMRP, Expiry, txtExpiry, StockList

        Label(root, text='Add Product', bg='#f1eff0', font=('Verdana', 40, 'bold'), justify=CENTER).place(x=500, y=20)

        Barcode = StringVar()
        Label(root, text='Barcode', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=450)
        txtBarcode = Entry(root, textvariable=Barcode, font=15)
        txtBarcode.place(x=250, y=460)

        ItemName = StringVar()
        Label(root, text='Item Name', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=150)
        txtItemName = Entry(root, textvariable=ItemName, font=15)
        txtItemName.place(x=250, y=160)

        Weight = StringVar()
        Label(root, text='Weight', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=200)
        txtWeight = Entry(root, textvariable=Weight, font=15)
        txtWeight.place(x=250, y=210)

        ItemType = StringVar()
        Label(root, text='Item Type', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=250)
        txtItemType = Entry(root, textvariable=ItemType, font=15)
        txtItemType.place(x=250, y=260)

        Quantity = StringVar()
        CheckPin = root.register(onlynum)
        Label(root, text='Quantity', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=300)
        txtQuantity = Entry(root, textvariable=Quantity, font=15)
        txtQuantity.place(x=250, y=310)
        txtQuantity.configure(validate='key', validatecommand=(CheckPin, '%P'))

        MRP = StringVar()
        Label(root, text='M.R.P.', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=350)
        txtMRP = Entry(root, textvariable=MRP, font=15)
        txtMRP.place(x=250, y=360)

        Expiry = StringVar()
        Label(root, text='Expiry Date', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=400)
        txtExpiry = Entry(root, textvariable=Expiry, font=15)
        txtExpiry.place(x=250, y=410)

        ItemRef = StringVar()
        Label(root, text='Item Ref', bg='#f1eff0', font=('Verdana', 15)).place(x=100, y=500)
        txtItemRef = Label(root, textvariable=ItemRef, font=15)
        txtItemRef.place(x=250, y=510)
    except Exception:
        pass


AddStockButtonPhoto = PhotoImage(file=r"images/addstock.png")
AddBtn = Button(root, text='Add Stock', image=AddStockButtonPhoto, command=AddStock)
AddBtn.place(x=550, y=550)
AddBtnTTP = ToolTipText.CreateToolTip(AddBtn, 'Add Product')

UpdateStockButtonPhoto = PhotoImage(file=r"images/updatestock.png")
UpdtBtn = Button(root, text='Update Stock', image=UpdateStockButtonPhoto, command=Update)
UpdtBtn.place(x=650, y=550)
UpdtBtnTTP = ToolTipText.CreateToolTip(UpdtBtn, 'Go to Update Stock Menu from here.')

DeleteStockButtonPhoto = PhotoImage(file=r"images/deletestock.png")
DltBtn = Button(root, text='Delete Stock', image=DeleteStockButtonPhoto, command=Delete)
DltBtn.place(x=750, y=550)
DltBtnTTP = ToolTipText.CreateToolTip(DltBtn, 'Go to Delete Product Menu from here.')

RegisterButtonPhoto = PhotoImage(file=r"images/register.png")
RegBtn = Button(root, text='Register', image=RegisterButtonPhoto, command=Register)
RegBtn.place(x=850, y=550)
RegBtnTTP = ToolTipText.CreateToolTip(RegBtn, 'Go to User Registeration Menu from here.')

ResetButtonPhoto = PhotoImage(file=r"images/reset.png")
ResBtn = Button(root, text='Reset', image=ResetButtonPhoto, command=clearvalues)
ResBtn.place(x=950, y=550)
ResBtnTTP = ToolTipText.CreateToolTip(ResBtn, 'Reset this form')

DownRepButtonPhoto = PhotoImage(file=r'images/downloadreport.png')
DownRepBtn = Button(root, text='Save Report', command=saverep, image=DownRepButtonPhoto)
DownRepBtn.place(x=1050, y=550)

root.bind('<Control-S>', AddStock)
root.bind('<Control-s>', AddStock)
root.bind('<Control-D>', Delete)
root.bind('<Control-d>', Delete)
root.bind('<Control-U>', Update)
root.bind('<Control-u>', Update)
root.bind('<Control-N>', Register)
root.bind('<Control-n>', Register)

# display()
Design()
root.mainloop()
