from tkinter import *
from tkinter import messagebox
import ToolTipText
import DataBase

root = Tk()
root.state('zoomed')
root.title('Stock Maintenance')
root.resizable(False, False)
root.iconbitmap("images/deletestock.ico")
image1 = PhotoImage(file="images/DeleteProduct.png")
label_for_image = Label(root, image=image1)
label_for_image.pack()
frameAvailableStockData = Frame(root, bd=4, relief='raise')
frameAvailableStockData.place(x=300, y=330)

StockMaintain = DataBase.Stock()
ObjStockView = DataBase.AvailableStockView()


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)

ObjStockView.view(frameAvailableStockData, ObjStockView.scroll_view, 20, ObjStockView.onmousewheel)
ObjStockView.display(StockMaintain)


def Add(event=''):
        root.destroy()
        try:
            import AddProduct
            a = AddProduct.Design()
        except Exception:
            pass


def Update(event=''):
    root.destroy()
    try:
        import UpdateProduct
        a = UpdateProduct.Design()
    except Exception:
        pass


def Delete():
    StockMaintain.delete(z)
    messagebox.showinfo('Information', z + ' has been deleted successfully.')
    ObjStockView.display(StockMaintain)
    refreshdelete()


def search(event=''):
    if optvar.get() != '':
        rows = StockMaintain.Search(optvar.get())
        refreshdelete()
        index = 0
        for i in rows:
            index += 1
            lstBarcode.insert(index,i[0])
            lstItemRef.insert(index, i[1])
            lstItemName.insert(index, i[2])
            lstItemType.insert(index, i[3])
            lstQuantity.insert(index, i[4])
            lstMRP.insert(index, i[5])
            lstExpiry.insert(index, i[6])
    elif optvar.get() == '':
        messagebox.showerror('Error', 'No such product.')


def refreshdelete():
    optvar.set('')
    lstBarcode.delete(0,END)
    lstItemRef.delete(0, END)
    lstItemName.delete(0, END)
    lstItemType.delete(0, END)
    lstQuantity.delete(0, END)
    lstMRP.delete(0, END)
    lstExpiry.delete(0, END)


def select(event):
        global z
        p = lstItemRef.curselection()[0]
        sd = lstItemRef.get(p)
        sc = lstQuantity.get(p)
        z = sd[0:]
        b = sc[0:]
        q = messagebox.askyesno('Information',
                                'Do you really wish to delete "' + z + '",available stock is ' + b + '. Click "Yes" to Delete else "No".')
        if q > 0:
            StockMaintain.delete(z)
            messagebox.showinfo('Information', 'Product ' + z + ' has been successfully deleted from your stock.')
            ObjStockView.display(StockMaintain)
            refreshdelete()


frameStockData = Frame(root, bd=4, relief='raise')
frameStockData.place(x=305, y=180)
optvar = StringVar()
Entry(root, textvariable=optvar).place(x=530, y=130)
Label(root, text='Delete Product', bg='#efefef', font=('Verdana', 40, 'bold'), justify=CENTER).place(x=460, y=20)


def DeleteStockView():
    def scroll_view(*args):
        lstBarcode.yview(*args)
        lstItemName.yview(*args)
        lstItemType.yview(*args)
        lstQuantity.yview(*args)
        lstMRP.yview(*args)
        lstExpiry.yview(*args)
        lstItemRef.yview(*args)
    global lstBarcode, lstItemRef, lstItemName, lstItemType, lstQuantity, lstMRP, lstExpiry

    scrollbar = Scrollbar(frameStockData, command=scroll_view)
    scrollbar.grid(row=1, column=7, sticky=N + S)
    lblBarcode = Label(frameStockData, text='Barcode')
    lblBarcode.grid(row=0, column=0)
    lstBarcode = Listbox(frameStockData, width=15, height=5, yscrollcommand=scrollbar.set)
    lstBarcode.grid(row=1, column=0)
    lblItemRef = Label(frameStockData, text='Item Ref')
    lblItemRef.grid(row=0, column=1)
    lstItemRef = Listbox(frameStockData, width=20, height=5, yscrollcommand=scrollbar.set)
    lstItemRef.grid(row=1, column=1)
    lblItemName = Label(frameStockData, text='Item Name')
    lblItemName.grid(row=0, column=2)
    lstItemName = Listbox(frameStockData, width=30, height=5, yscrollcommand=scrollbar.set)
    lstItemName.grid(row=1, column=2)
    lstItemRef.bind('<<ListboxSelect>>', select)
    lblItemType = Label(frameStockData, text='Item Type')
    lblItemType.grid(row=0, column=3)
    lstItemType = Listbox(frameStockData, width=20, height=5, yscrollcommand=scrollbar.set)
    lstItemType.grid(row=1, column=3)
    lblQuantity = Label(frameStockData, text='Stock')
    lblQuantity.grid(row=0, column=4)
    lstQuantity = Listbox(frameStockData, width=5, height=5, yscrollcommand=scrollbar.set)
    lstQuantity.grid(row=1, column=4)
    lblMRP = Label(frameStockData, text='M.R.P.')
    lblMRP.grid(row=0, column=5)
    lstMRP = Listbox(frameStockData, width=8, height=5, yscrollcommand=scrollbar.set)
    lstMRP.grid(row=1, column=5)
    lblExpiry = Label(frameStockData, text='Expiry Date')
    lblExpiry.grid(row=0, column=6)
    lstExpiry = Listbox(frameStockData, width=15, height=5, yscrollcommand=scrollbar.set)
    lstExpiry.grid(row=1, column=6)


AddStockButtonPhoto = PhotoImage(file=r"images/addstock.png")
AddBtn = Button(root, text='Add Stock', image=AddStockButtonPhoto, command=Add)
AddBtn.place(x=1100, y=400)
AddBtnTTP = ToolTipText.CreateToolTip(AddBtn, 'Go to Add Product Menu from here.')

UpdateStockButtonPhoto = PhotoImage(file=r"images/updatestock.png")
UpdtBtn = Button(root, text='Update Stock', image=UpdateStockButtonPhoto, command=Update)
UpdtBtn.place(x=1100, y=500)
UpdtBtnTTP = ToolTipText.CreateToolTip(UpdtBtn, 'Go to Update Stock Menu from here.')

SearchStockButtonPhoto = PhotoImage(file=r"images/SearchIcon.png")
SrchBtn = Button(root, text='Search', image=SearchStockButtonPhoto, command=search)
SrchBtn.place(x=725, y=125)
SrchBtnTTP = ToolTipText.CreateToolTip(SrchBtn, 'Search Product')

DeleteStockView()

root.bind('<Control-A>', Add)
root.bind('<Control-a>', Add)
root.bind('<Control-U>', Update)
root.bind('<Control-u>', Update)
root.bind('<Return>', search)

root.mainloop()
