import ToolTipText
from tkinter import *
from tkinter import messagebox
import DataBase

root = Tk()
root.state('zoomed')
root.resizable(False, False)
root.title('Stock Maintenance')
root.iconbitmap("images/updatestock.ico")
image1 = PhotoImage(file='images/UpdateProduct.png')
label_for_image = Label(root, image=image1)
label_for_image.pack()

StockMaintain = DataBase.Stock()
ObjStockView = DataBase.AvailableStockView()


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)

optvar = StringVar()
Entry(root, textvariable=optvar, width=25).place(x=530, y=130)


def search(event=''):
    if optvar.get() != '':
        row = StockMaintain.Search(optvar.get())
        txtItemName.delete(0, END)
        txtItemType.delete(0, END)
        Quantity.set('')
        txtNewStock.delete(0, END)
        txtMRP.delete(0, END)
        txtExpiry.delete(0, END)
        txtItemRef.delete(0, END)
        lstItemRef.delete(0, END)
        lstItemName.delete(0, END)
        lstItemType.delete(0, END)
        lstQuantity.delete(0, END)
        lstMRP.delete(0, END)
        lstExpiry.delete(0, END)
        lstBarcode.delete(0, END)
        index = 0
        for i in row:
            index += 1
            lstBarcode.insert(index, i[0])
            lstItemRef.insert(index, i[1])
            lstItemName.insert(index, i[2])
            lstItemType.insert(index, i[3])
            lstQuantity.insert(index, i[4])
            lstMRP.insert(index, i[5])
            lstExpiry.insert(index, i[6])
    else:
        messagebox.showerror('Error', 'No such product.')


def refresh(event=''):
    txtItemName.delete(0, END)
    txtItemType.delete(0, END)
    Quantity.set(0)
    txtNewStock.delete(0, END)
    txtMRP.delete(0, END)
    txtExpiry.delete(0, END)
    txtItemRef.delete(0, END)
    txtBarcode.delete(0,END)
    lstBarcode.delete(0,END)
    lstItemRef.delete(0, END)
    lstItemName.delete(0, END)
    lstItemType.delete(0, END)
    lstQuantity.delete(0, END)
    lstMRP.delete(0, END)
    lstExpiry.delete(0, END)
    optvar.set('')


def onlynum(e):
    if e.isdigit():
        return True
    elif e == '':
        return True
    else:
        return False


def update(event=''):
    stoc = int(txtNewStock.get())
    lis=int(txtQuantity.cget('text'))
    upd=lis+stoc
    StockMaintain.update(txtItemRef, txtItemName, txtItemType, upd, MRP, txtExpiry)
    if txtNewStock.get() != '':
        a = messagebox.askyesno('Information', 'Your existing stock for ' + str(txtItemName.get()) + ' of ' + str(
            lis) + ' will be updated to ' + str(upd) + '. If you wish to update click "Yes" else click "No".')
        if a > 0:
            StockMaintain.com()
            messagebox.showinfo('Information', 'Your stock for ' + str(txtItemName.get()) + ' of ' + str(
                lis) + ' is updated to ' + str(upd) + '.')
            refresh()
            ObjStockView.display(StockMaintain)


def select(event):
    p = lstItemRef.curselection()[0]
    sIN = lstItemName.get(p)
    sIR = lstItemRef.get(p)
    sIT = lstItemType.get(p)
    sQ = lstQuantity.get(p)
    sMRP = lstMRP.get(p)
    sExpiry = lstExpiry.get(p)
    sBarCode = lstBarcode.get(p)
    txtItemName.insert(END, sIN[0:])
    txtItemRef.insert(END, sIR[0:])
    txtItemType.insert(END, sIT[0:])
    Quantity.set(sQ[0:])
    txtMRP.insert(END, sMRP[0:])
    txtExpiry.insert(END, sExpiry[0:])
    txtBarcode.insert(END, sBarCode[0:])


frameUpdateStockData = Frame(root, bd=4, relief='raise')
frameUpdateStockData.place(x=305, y=180)

frameStockData = Frame(root, bd=4, relief='raise')
frameStockData.place(x=530, y=330)


def UpdateStockView():
    def scroll_view(*args):
        lstBarcode.yview(*args)
        lstItemName.yview(*args)
        lstItemType.yview(*args)
        lstQuantity.yview(*args)
        lstMRP.yview(*args)
        lstExpiry.yview(*args)
        lstItemRef.yview(*args)

    global lstBarcode, lstItemRef, lstItemName, lstItemType, lstQuantity, lstMRP, lstExpiry

    scrollbar = Scrollbar(frameUpdateStockData, command=scroll_view)
    scrollbar.grid(row=1, column=7, sticky=N + S)
    lblBarcode = Label(frameUpdateStockData, text='Barcode')
    lblBarcode.grid(row=0, column=0)
    lstBarcode = Listbox(frameUpdateStockData, width=15, height=5, yscrollcommand=scrollbar.set)
    lstBarcode.grid(row=1, column=0)
    lblItemRef = Label(frameUpdateStockData, text='Item Ref')
    lblItemRef.grid(row=0, column=1)
    lstItemRef = Listbox(frameUpdateStockData, width=20, height=5, yscrollcommand=scrollbar.set)
    lstItemRef.grid(row=1, column=1)
    lblItemName = Label(frameUpdateStockData, text='Item Name')
    lblItemName.grid(row=0, column=2)
    lstItemName = Listbox(frameUpdateStockData, width=30, height=5, yscrollcommand=scrollbar.set)
    lstItemName.grid(row=1, column=2)
    lstItemRef.bind('<<ListboxSelect>>', select)
    lblItemType = Label(frameUpdateStockData, text='Item Type')
    lblItemType.grid(row=0, column=3)
    lstItemType = Listbox(frameUpdateStockData, width=20, height=5, yscrollcommand=scrollbar.set)
    lstItemType.grid(row=1, column=3)
    lblQuantity = Label(frameUpdateStockData, text='Stock')
    lblQuantity.grid(row=0, column=4)
    lstQuantity = Listbox(frameUpdateStockData, width=5, height=5, yscrollcommand=scrollbar.set)
    lstQuantity.grid(row=1, column=4)
    lblMRP = Label(frameUpdateStockData, text='M.R.P.')
    lblMRP.grid(row=0, column=5)
    lstMRP = Listbox(frameUpdateStockData, width=8, height=5, yscrollcommand=scrollbar.set)
    lstMRP.grid(row=1, column=5)
    lblExpiry = Label(frameUpdateStockData, text='Expiry Date')
    lblExpiry.grid(row=0, column=6)
    lstExpiry = Listbox(frameUpdateStockData, width=15, height=5, yscrollcommand=scrollbar.set)
    lstExpiry.grid(row=1, column=6)


ObjStockView.view(frameStockData, ObjStockView.scroll_view, 20, ObjStockView.onmousewheel)
ObjStockView.display(StockMaintain)


def Add(event=''):
    root.destroy()
    try:
        import AddProduct
        a = AddProduct.Design()
    except Exception:
        pass

def Delete(event=''):
    root.destroy()
    try:
        import DeleteProduct
        a = DeleteProduct.DeleteStockView()
    except Exception:
        pass

UpdateStockView()


def Design():
    global frameStockData, ItemRef, txtItemRef, ItemName, txtItemName, txtNewStock, Weight, txtWeight, ItemType, txtItemType, Quantity, txtQuantity, MRP, txtMRP, Expiry, txtExpiry, StockList, txtBarcode

    Label(root, text='Update Stock', bg='#e2e3dd', font=('Verdana', 40, 'bold'), justify=CENTER).place(x=470, y=20)

    ItemName = StringVar()
    Label(root, text='Item Name', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=320)
    txtItemName = Entry(root, textvariable=ItemName, font=15)
    txtItemName.place(x=230, y=330)

    ItemType = StringVar()
    Label(root, text='Item Type', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=370)
    txtItemType = Entry(root, textvariable=ItemType, font=15)
    txtItemType.place(x=230, y=380)

    Quantity = StringVar()
    Quantity.set(0)
    Label(root, text='Existing Stock', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=420)
    txtQuantity = Label(root, textvariable=Quantity, font=15, bg='#e2e3dd')
    txtQuantity.place(x=230, y=425)

    CheckText = root.register(onlynum)
    NewStock = StringVar()
    Label(root, text='Add More', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=470)
    txtNewStock = Entry(root, textvariable=NewStock, font=15)
    txtNewStock.place(x=230, y=480)
    txtNewStock.configure(validate='key', validatecommand=(CheckText, '%P'))

    MRP = StringVar()
    Label(root, text='M.R.P.', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=520)
    txtMRP = Entry(root, textvariable=MRP, font=15)
    txtMRP.place(x=230, y=530)

    Expiry = StringVar()
    Label(root, text='Expiry Date', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=570)
    txtExpiry = Entry(root, textvariable=Expiry, font=15)
    txtExpiry.place(x=230, y=580)

    ItemRef = StringVar()
    Label(root, text='Item Ref.', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=620)
    txtItemRef = Entry(root, textvariable=ItemRef, font=15)
    txtItemRef.place(x=230, y=630)

    Barcode = StringVar()
    Label(root, text='Barcode', bg='#e2e3dd', font=('Verdana', 15)).place(x=70, y=670)
    txtBarcode = Entry(root, textvariable=Barcode, font=15)
    txtBarcode.place(x=230, y=680)


Design()

AddStockButtonPhoto = PhotoImage(file=r"images/addstock.png")
AddBtn = Button(root, text='Add Stock', image=AddStockButtonPhoto, command=Add)
AddBtn.place(x=1200, y=200)
AddBtnTTP = ToolTipText.CreateToolTip(AddBtn, 'Go to Add Product Menu from here.')

UpdateStockButtonPhoto = PhotoImage(file=r"images/updatestock.png")
UpdtBtn = Button(root, text='Update Stock', image=UpdateStockButtonPhoto, command=update)
UpdtBtn.place(x=440, y=400)
UpdtBtnTTP = ToolTipText.CreateToolTip(UpdtBtn, 'Update Stock')

DeleteStockButtonPhoto = PhotoImage(file=r"images/deletestock.png")
DltBtn = Button(root, text='Delete Stock', image=DeleteStockButtonPhoto, command=Delete)
DltBtn.place(x=1100, y=200)
DltBtnTTP = ToolTipText.CreateToolTip(DltBtn, 'Go to Delete Product Menu from here.')

SearchStockButtonPhoto = PhotoImage(file=r"images/SearchIcon.png")
SrchBtn = Button(root, text='Search', image=SearchStockButtonPhoto, command=search)
SrchBtn.place(x=725, y=125)
SrchBtnTTP = ToolTipText.CreateToolTip(SrchBtn, 'Search Product')

ResetButtonPhoto = PhotoImage(file=r"images/reset.png")
ResBtn = Button(root,  text='Reset', image=ResetButtonPhoto,command=refresh)
ResBtn.place(x=440, y=500)

root.bind('<Control-S>', update)
root.bind('<Control-s>', update)
root.bind('<Control-D>', Delete)
root.bind('<Control-d>', Delete)
root.bind('<Control-A>', Add)
root.bind('<Control-a>', Add)
root.bind('<Return>',search)
root.bind('<F5>',refresh)
root.mainloop()
