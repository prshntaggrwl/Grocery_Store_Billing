from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import random
from datetime import datetime
import tempfile
import os
import DataBase
import ToolTipText
from pygame import mixer

root = Tk()
mixer.init()
root.state('zoomed')
root.resizable(False, False)
root.iconbitmap("images/generateBill.ico")
image1 = PhotoImage(file="images/helena-lopes-ZRpaul1m-DY-unsplash.png")
label_for_image = Label(root, image=image1)
label_for_image.pack()


def on_close_win():
    if messagebox.askyesno('Confirm Exit', 'Do you really want to quit?'):
        reset()
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_win)


class salesreport:
    def __init__(self):
        self.conn = sqlite3.connect('Grocery.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS SalesReport(BillNum,CustomerName TEXT,Mobile TEXT,Address TEXT,List1Product,List2Product,List3Product,List4Product,List5Product,List6Product,List7Product,List8Product,List9Product,List10Product)')
        self.conn.commit()

    def insert(self, BillNum, CustName, CustMobile, CustAddress, Item1Detail, Item2Detail, Item3Detail, Item4Detail,
               Item5Detail, Item6Detail, Item7Detail, Item8Detail, Item9Detail, Item10Detail):
        self.cur.execute('INSERT INTO SalesReport VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
            BillNum, CustName, CustMobile, CustAddress, Item1Detail, Item2Detail, Item3Detail, Item4Detail, Item5Detail,
            Item6Detail, Item7Detail, Item8Detail, Item9Detail, Item10Detail))
        self.conn.commit()

    def update(self, Stock=''):
        self.cur.execute('UPDATE StockDetails SET Stock=?', Stock)
        self.conn.commit()


SalesSave = salesreport()

ObjViewStore = DataBase.Store()
ObjViewStock = DataBase.Stock()


def scroll_view_search_view(*args):
    ItemrefView.yview(*args)
    ItemnameView.yview(*args)
    ItemtypeView.yview(*args)


def design():
    try:
        global txtItemRef, txtBill, CustName, CustMobile, CustAddress, AddQty, lblTry, LablTry, FrameBill, BillEG, opt, array, ItemrefView, ItemnameView, ItemtypeView
        for i in ObjViewStore.view():
            a = i[0]
            Label(root, text=a, font=('Verdana', 40, 'bold'), bg='#e0e5e8', justify=CENTER).place(x=370, y=20)
            root.title(a)
        Label(root, text='Name', relief='raise', font=('Verdana', 15)).place(x=520, y=420)
        CName = StringVar()
        CustName = Entry(root, textvariable=CName, width=25)
        CustName.place(x=620, y=423)
        Label(root, text='Mobile', relief='raise', font=('Verdana', 15)).place(x=520, y=470)
        CMobile = StringVar()
        CustMobile = Entry(root, textvariable=CMobile, width=25)
        CheckMob = root.register(onlyNum)
        CustMobile.configure(validate='key', validatecommand=(CheckMob, '%P'))
        CustMobile.place(x=620, y=473)
        Label(root, text='Enter product', relief='raise', font=('Verdana', 15)).place(x=30, y=120)
        Label(root, text='Quantity', relief='raise', font=('Verdana', 15)).place(x=30, y=200)
        txtItemRef = StringVar()
        w = Entry(root, textvariable=txtItemRef)
        w.place(x=30, y=160)
        w.bind('<KeyRelease>', caps)
        CheckQty = root.register(onlyNum)
        AddQty = Entry(root)
        AddQty.configure(validate='key', validatecommand=(CheckQty, '%P'))
        AddQty.place(x=30, y=240)
        frmBill = Frame(root)
        frmBill.place(x=920, y=350)
        scrollbill = Scrollbar(frmBill)
        scrollbill.pack(side=RIGHT, fill=Y)
        BillEG = Text(frmBill, width=50, height=23, yscrollcommand=scrollbill.set)
        BillEG.pack()
        scrollbill.config(command=BillEG.yview)
        frameStockData = LabelFrame(root, text='Select Item here:', bd=4, relief='raise')
        frameStockData.place(x=50, y=370)
        scrollbar = Scrollbar(frameStockData, command=scroll_view_search_view)
        scrollbar.grid(row=1, column=7, sticky=N + S)
        lblItemRefView = Label(frameStockData, text='Item Ref')
        lblItemRefView.grid(row=0, column=0)

        ItemrefView = Listbox(frameStockData, width=13, height=5, yscrollcommand=scrollbar.set)
        ItemrefView.grid(row=1, column=0)
        ItemrefView.bind('<<ListboxSelect>>', test)

        lblItemNameView = Label(frameStockData, text='Item Name')
        lblItemNameView.grid(row=0, column=1)
        ItemnameView = Listbox(frameStockData, width=35, height=5, yscrollcommand=scrollbar.set)
        ItemnameView.grid(row=1, column=1)
        lblItemTypeView = Label(frameStockData, text='Item Type')
        lblItemTypeView.grid(row=0, column=3)
        ItemtypeView = Listbox(frameStockData, width=20, height=5, yscrollcommand=scrollbar.set)
        ItemtypeView.grid(row=1, column=3)
    except Exception:
        pass


def onlyNum(e):
    if e.isdigit():
        return True
    elif e == '':
        return True
    else:
        return False


def caps(event):
    txtItemRef.set(txtItemRef.get().upper())


def iPrint():
    q = BillEG.get('1.0', 'end-1c')
    filename = tempfile.mktemp('.txt')
    open(filename, 'w').write(q)
    os.startfile(filename, 'print')


def reduce(a):
    conn = sqlite3.connect('Grocery.db')
    cur = conn.cursor()
    sel = cur.execute('SELECT Stock,ItemName FROM StockDetails WHERE ItemName=?', (a,))
    for stoc in sel:
        lisred = stoc[0]
    lisred = int(lisred)
    stoc = 1
    upd = lisred + stoc
    cur.execute('UPDATE StockDetails SET Stock=? WHERE ItemName=?', (upd, a))
    conn.commit()
    Qty1.set(int(Qty1.get()) - 1)
    Total1.set(int(MRP1var.get()) * int(Qty1.get()))
    displayStockView()
    FinlAmount.set('Total Amount: ' + str(
        int(MRP1var.get()) * int(Qty1.get()) + int(MRP2var.get()) * int(Qty2.get()) + int(MRP3var.get()) * int(
            Qty3.get()) + int(MRP4var.get()) * int(Qty4.get()) + int(MRP5var.get()) * int(Qty5.get()) + int(
            MRP6var.get()) * int(Qty6.get()) + int(MRP7var.get()) * int(Qty7.get()) + int(MRP8var.get()) * int(
            Qty8.get()) + int(MRP9var.get()) * int(Qty9.get()) + int(MRP10var.get()) * int(Qty10.get())))


def reduce1():
    reduce(ItmNm1.get())


def reduce2():
    reduce(ItmNm2.get())


def reduce3():
    reduce(ItmNm3.get())


def reduce4():
    reduce(ItmNm4.get())


def reduce5():
    reduce(ItmNm5.get())


def reduce6():
    reduce(ItmNm6.get())


def reduce7():
    reduce(ItmNm7.get())


def reduce8():
    reduce(ItmNm8.get())


def reduce9():
    reduce(ItmNm9.get())


def reduce10():
    reduce(ItmNm10.get())


def add(a):
    conn = sqlite3.connect('Grocery.db')
    cur = conn.cursor()
    sel = cur.execute('SELECT Stock,ItemName FROM StockDetails WHERE ItemName=?', (a,))
    for stoc in sel:
        lisadd = stoc[0]
    lisadd = int(lisadd)
    stoc = 1
    upd = lisadd - stoc
    cur.execute('UPDATE StockDetails SET Stock=? WHERE ItemName=?', (upd, a))
    conn.commit()
    Qty1.set(int(Qty1.get()) + 1)
    Total1.set(int(MRP1var.get()) * int(Qty1.get()))
    displayStockView()
    FinlAmount.set('Total Amount: ' + str(
        int(MRP1var.get()) * int(Qty1.get()) + int(MRP2var.get()) * int(Qty2.get()) + int(MRP3var.get()) * int(
            Qty3.get()) + int(MRP4var.get()) * int(Qty4.get()) + int(MRP5var.get()) * int(Qty5.get()) + int(
            MRP6var.get()) * int(Qty6.get()) + int(MRP7var.get()) * int(Qty7.get()) + int(MRP8var.get()) * int(
            Qty8.get()) + int(MRP9var.get()) * int(Qty9.get()) + int(MRP10var.get()) * int(Qty10.get())))


def add1():
    add(ItmNm1.get())


def add2():
    add(ItmNm2.get())


def add3():
    add(ItmNm3.get())


def add4():
    add(ItmNm4.get())


def add5():
    add(ItmNm5.get())


def add6():
    add(ItmNm6.get())


def add7():
    add(ItmNm7.get())


def add8():
    add(ItmNm8.get())


def add9():
    add(ItmNm9.get())


def add10():
    add(ItmNm10.get())


def prolist():
    global BtnM1, BtnA1, BtnM2, BtnA2, BtnM3, BtnA3, BtnM4, BtnA4, BtnM5, BtnA5, BtnM6, BtnA6, BtnM7, BtnA7, BtnM8, BtnA8, BtnM9, BtnA9, BtnM10, BtnA10, ItmNm1, MRP1var, Qty1, Total1, ItmNm2, MRP2var, Qty2, Total2, ItmNm3, MRP3var, Qty3, Total3, ItmNm4, MRP4var, Qty4, Total4, ItmNm5, MRP5var, Qty5, Total5, ItmNm6, MRP6var, Qty6, Total6, ItmNm7, MRP7var, Qty7, Total7, ItmNm8, MRP8var, Qty8, Total8, ItmNm9, MRP9var, Qty9, Total9, ItmNm10, MRP10var, Qty10, Total10, FinlAmount
    Label(root, text='Item Name', bg='#e0e5e8', relief='raise').place(x=210, y=120)
    Label(root, text='Price', bg='#e0e5e8', relief='raise').place(x=370, y=120)
    Label(root, text='Qty.', bg='#e0e5e8', relief='raise').place(x=420, y=120)
    Label(root, text='Total', bg='#e0e5e8', relief='raise').place(x=460, y=120)
    Label(root, text='1)', relief='raise').place(x=185, y=150)
    ItmNm1 = StringVar()
    ItemName1 = Label(root, textvariable=ItmNm1, anchor='w', relief='raise', width=20)
    ItemName1.place(x=210, y=150)
    MRP1var = StringVar()
    MRP1 = Label(root, width=4, textvariable=MRP1var, relief='raise')
    MRP1.place(x=370, y=150)
    MRP1var.set(0)
    Qty1 = StringVar()
    Quantity1 = Label(root, width=3, textvariable=Qty1, relief='raise')
    Quantity1.place(x=420, y=150)
    Qty1.set(0)
    Total1 = StringVar()
    TotalAmt1 = Label(root, width=4, textvariable=Total1, relief='raise')
    TotalAmt1.place(x=460, y=150)
    BtnM1 = Button(root, text='-', command=reduce1, state=DISABLED)
    BtnM1.place(x=510, y=148)
    BtnA1 = Button(root, text='+', state=DISABLED, command=add1)
    BtnA1.place(x=540, y=148)

    Label(root, text='2)', relief='raise').place(x=185, y=190)
    ItmNm2 = StringVar()
    ItemName2 = Label(root, textvariable=ItmNm2, relief='raise', width=20)
    ItemName2.place(x=210, y=190)
    MRP2var = StringVar()
    MRP2 = Label(root, textvariable=MRP2var, width=4, relief='raise')
    MRP2.place(x=370, y=190)
    MRP2var.set(0)
    Qty2 = StringVar()
    Quantity2 = Label(root, textvariable=Qty2, width=3, relief='raise')
    Quantity2.place(x=420, y=190)
    Qty2.set(0)
    Total2 = StringVar()
    TotalAmt2 = Label(root, width=4, textvariable=Total2, relief='raise')
    TotalAmt2.place(x=460, y=190)
    BtnM2 = Button(root, text='-', state=DISABLED, command=reduce2)
    BtnM2.place(x=510, y=188)
    BtnA2 = Button(root, text='+', state=DISABLED, command=add2)
    BtnA2.place(x=540, y=188)

    Label(root, text='3)', relief='raise').place(x=185, y=230)
    ItmNm3 = StringVar()
    ItemName3 = Label(root, textvariable=ItmNm3, relief='raise', width=20)
    ItemName3.place(x=210, y=230)
    MRP3var = StringVar()
    MRP3 = Label(root, textvariable=MRP3var, width=4, relief='raise')
    MRP3.place(x=370, y=230)
    MRP3var.set(0)
    Qty3 = StringVar()
    Quantity3 = Label(root, textvariable=Qty3, width=3, relief='raise')
    Quantity3.place(x=420, y=230)
    Qty3.set(0)
    Total3 = StringVar()
    TotalAmt3 = Label(root, width=4, textvariable=Total3, relief='raise')
    TotalAmt3.place(x=460, y=230)
    BtnM3 = Button(root, text='-', state=DISABLED, command=reduce3)
    BtnM3.place(x=510, y=228)
    BtnA3 = Button(root, text='+', state=DISABLED, command=add3)
    BtnA3.place(x=540, y=228)

    Label(root, text='4)', relief='raise').place(x=185, y=270)
    ItmNm4 = StringVar()
    ItemName4 = Label(root, textvariable=ItmNm4, relief='raise', width=20)
    ItemName4.place(x=210, y=270)
    MRP4var = StringVar()
    MRP4 = Label(root, textvariable=MRP4var, width=4, relief='raise')
    MRP4.place(x=370, y=270)
    MRP4var.set(0)
    Qty4 = StringVar()
    Quantity4 = Label(root, textvariable=Qty4, width=3, relief='raise')
    Quantity4.place(x=420, y=270)
    Qty4.set(0)
    Total4 = StringVar()
    TotalAmt4 = Label(root, width=4, textvariable=Total4, relief='raise')
    TotalAmt4.place(x=460, y=270)
    BtnM4 = Button(root, text='-', state=DISABLED, command=reduce4)
    BtnM4.place(x=510, y=268)
    BtnA4 = Button(root, text='+', state=DISABLED, command=add4)
    BtnA4.place(x=540, y=268)

    Label(root, text='5)', relief='raise').place(x=185, y=310)
    ItmNm5 = StringVar()
    ItemName5 = Label(root, textvariable=ItmNm5, relief='raise', width=20)
    ItemName5.place(x=210, y=310)
    MRP5var = StringVar()
    MRP5 = Label(root, textvariable=MRP5var, width=4, relief='raise')
    MRP5.place(x=370, y=310)
    MRP5var.set(0)
    Qty5 = StringVar()
    Quantity5 = Label(root, textvariable=Qty5, width=3, relief='raise')
    Quantity5.place(x=420, y=310)
    Qty5.set(0)
    Total5 = StringVar()
    TotalAmt5 = Label(root, width=4, textvariable=Total5, relief='raise')
    TotalAmt5.place(x=460, y=310)
    BtnM5 = Button(root, text='-', state=DISABLED, command=reduce5)
    BtnM5.place(x=510, y=308)
    BtnA5 = Button(root, text='+', state=DISABLED, command=add5)
    BtnA5.place(x=540, y=308)

    Label(root, text='Item Name', bg='#e0e5e8', relief='raise').place(x=610, y=120)
    Label(root, text='M.R.P', bg='#e0e5e8', relief='raise').place(x=770, y=120)
    Label(root, text='Qty.', bg='#e0e5e8', relief='raise').place(x=820, y=120)
    Label(root, text='Total', bg='#e0e5e8', relief='raise').place(x=860, y=120)
    Label(root, text='6)', relief='raise').place(x=590, y=150)
    ItmNm6 = StringVar()
    ItemName6 = Label(root, textvariable=ItmNm6, relief='raise', width=20)
    ItemName6.place(x=610, y=150)
    MRP6var = StringVar()
    MRP6 = Label(root, textvariable=MRP6var, width=4, relief='raise')
    MRP6.place(x=770, y=150)
    MRP6var.set(0)
    Qty6 = StringVar()
    Quantity6 = Label(root, textvariable=Qty6, width=3, relief='raise')
    Quantity6.place(x=820, y=150)
    Qty6.set(0)
    Total6 = StringVar()
    TotalAmt6 = Label(root, width=4, textvariable=Total6, relief='raise')
    TotalAmt6.place(x=860, y=150)
    BtnM6 = Button(root, text='-', state=DISABLED, command=reduce6)
    BtnM6.place(x=910, y=148)
    BtnA6 = Button(root, text='+', state=DISABLED, command=add6)
    BtnA6.place(x=940, y=148)

    Label(root, text='7)', relief='raise').place(x=590, y=190)
    ItmNm7 = StringVar()
    ItemName7 = Label(root, textvariable=ItmNm7, relief='raise', width=20)
    ItemName7.place(x=610, y=190)
    MRP7var = StringVar()
    MRP7 = Label(root, textvariable=MRP7var, width=4, relief='raise')
    MRP7.place(x=770, y=190)
    MRP7var.set(0)
    Qty7 = StringVar()
    Quantity7 = Label(root, textvariable=Qty7, width=3, relief='raise')
    Quantity7.place(x=820, y=190)
    Qty7.set(0)
    Total7 = StringVar()
    TotalAmt7 = Label(root, width=4, textvariable=Total7, relief='raise')
    TotalAmt7.place(x=860, y=190)
    BtnM7 = Button(root, text='-', state=DISABLED, command=reduce7)
    BtnM7.place(x=910, y=188)
    BtnA7 = Button(root, text='+', state=DISABLED, command=add7)
    BtnA7.place(x=940, y=188)

    Label(root, text='8)', relief='raise').place(x=590, y=230)
    ItmNm8 = StringVar()
    ItemName8 = Label(root, textvariable=ItmNm8, relief='raise', width=20)
    ItemName8.place(x=610, y=230)
    MRP8var = StringVar()
    MRP8 = Label(root, textvariable=MRP8var, width=4, relief='raise')
    MRP8.place(x=770, y=230)
    MRP8var.set(0)
    Qty8 = StringVar()
    Quantity8 = Label(root, textvariable=Qty8, width=3, relief='raise')
    Quantity8.place(x=820, y=230)
    Qty8.set(0)
    Total8 = StringVar()
    TotalAmt8 = Label(root, width=4, textvariable=Total8, relief='raise')
    TotalAmt8.place(x=860, y=230)
    BtnM8 = Button(root, text='-', state=DISABLED, command=reduce8)
    BtnM8.place(x=910, y=228)
    BtnA8 = Button(root, text='+', state=DISABLED, command=add8)
    BtnA8.place(x=940, y=228)

    Label(root, text='9)', relief='raise').place(x=590, y=270)
    ItmNm9 = StringVar()
    ItemName9 = Label(root, textvariable=ItmNm9, relief='raise', width=20)
    ItemName9.place(x=610, y=270)
    MRP9var = StringVar()
    MRP9 = Label(root, textvariable=MRP9var, width=4, relief='raise')
    MRP9.place(x=770, y=270)
    MRP9var.set(0)
    Qty9 = StringVar()
    Quantity9 = Label(root, textvariable=Qty9, width=3, relief='raise')
    Quantity9.place(x=820, y=270)
    Qty9.set(0)
    Total9 = StringVar()
    TotalAmt9 = Label(root, width=4, textvariable=Total9, relief='raise')
    TotalAmt9.place(x=860, y=270)
    BtnM9 = Button(root, text='-', state=DISABLED, command=reduce9)
    BtnM9.place(x=910, y=268)
    BtnA9 = Button(root, text='+', state=DISABLED, command=add9)
    BtnA9.place(x=940, y=268)

    Label(root, text='10)', relief='raise').place(x=586, y=310)
    ItmNm10 = StringVar()
    ItemName10 = Label(root, textvariable=ItmNm10, relief='raise', width=20)
    ItemName10.place(x=610, y=310)
    MRP10var = StringVar()
    MRP10 = Label(root, textvariable=MRP10var, width=4, relief='raise')
    MRP10.place(x=770, y=310)
    MRP10var.set(0)
    Qty10 = StringVar()
    Quantity10 = Label(root, textvariable=Qty10, width=3, relief='raise')
    Quantity10.place(x=820, y=310)
    Qty10.set(0)
    Total10 = StringVar()
    TotalAmt10 = Label(root, width=4, textvariable=Total10, relief='raise')
    TotalAmt10.place(x=860, y=310)
    BtnM10 = Button(root, text='-', state=DISABLED, command=reduce10)
    BtnM10.place(x=910, y=308)
    BtnA10 = Button(root, text='+', state=DISABLED, command=add10)
    BtnA10.place(x=940, y=308)

    FinlAmount = StringVar()
    FinlAmount.set('Total Amount: ')
    Label(root, textvariable=FinlAmount, font=('Verdana', 20, 'bold'), anchor='w', relief='raise', width=20).place(
        x=520, y=370)


def addbill():
    try:
        conn = sqlite3.connect('Grocery.db')
        cur = conn.cursor()
        sel = cur.execute('SELECT ItemName,MRP,Stock FROM StockDetails WHERE ItemRef=?', (txtItemRef.get(),))
        for stoc in sel:
            lis = stoc[2]
        lis = int(lis)
        stoc = int(AddQty.get())
        upd = lis - stoc
        cur.execute('UPDATE StockDetails SET Stock=? WHERE ItemRef=?', (upd, txtItemRef.get(),))
        conn.commit()
        for i in ObjViewStock.Search(txtItemRef.get()):
            if ItmNm1.get() == '':
                ItmNm1.set(i[2])
                MRP1var.set(i[5])
                Qty1.set(AddQty.get())
                Total1.set(int(MRP1var.get()) * int(Qty1.get()))
                BtnM1.config(state=ACTIVE)
                BtnA1.config(state=ACTIVE)
            elif ItmNm2.get() == '':
                ItmNm2.set(i[2])
                MRP2var.set(i[5])
                Qty2.set(AddQty.get())
                Total2.set(int(MRP2var.get()) * int(Qty2.get()))
                BtnM2.config(state=ACTIVE)
                BtnA2.config(state=ACTIVE)
            elif ItmNm3.get() == '':
                ItmNm3.set(i[2])
                MRP3var.set(i[5])
                Qty3.set(AddQty.get())
                Total3.set(int(MRP3var.get()) * int(Qty3.get()))
                BtnM3.config(state=ACTIVE)
                BtnA3.config(state=ACTIVE)
            elif ItmNm4.get() == '':
                ItmNm4.set(i[2])
                MRP4var.set(i[5])
                Qty4.set(AddQty.get())
                Total4.set(int(MRP4var.get()) * int(Qty4.get()))
                BtnM4.config(state=ACTIVE)
                BtnA4.config(state=ACTIVE)
            elif ItmNm5.get() == '':
                ItmNm5.set(i[2])
                MRP5var.set(i[5])
                Qty5.set(AddQty.get())
                Total5.set(int(MRP5var.get()) * int(Qty5.get()))
                BtnM5.config(state=ACTIVE)
                BtnA5.config(state=ACTIVE)
            elif ItmNm6.get() == '':
                ItmNm6.set(i[2])
                MRP6var.set(i[5])
                Qty6.set(AddQty.get())
                Total6.set(int(MRP6var.get()) * int(Qty6.get()))
                BtnM6.config(state=ACTIVE)
                BtnA6.config(state=ACTIVE)
            elif ItmNm7.get() == '':
                ItmNm7.set(i[2])
                MRP7var.set(i[5])
                Qty7.set(AddQty.get())
                Total7.set(int(MRP7var.get()) * int(Qty7.get()))
                BtnM7.config(state=ACTIVE)
                BtnA7.config(state=ACTIVE)
            elif ItmNm8.get() == '':
                ItmNm8.set(i[2])
                MRP8var.set(i[5])
                Qty8.set(AddQty.get())
                Total8.set(int(MRP8var.get()) * int(Qty8.get()))
                BtnM8.config(state=ACTIVE)
                BtnA8.config(state=ACTIVE)
            elif ItmNm9.get() == '':
                ItmNm9.set(i[2])
                MRP9var.set(i[5])
                Qty9.set(AddQty.get())
                Total9.set(int(MRP9var.get()) * int(Qty9.get()))
                BtnM9.config(state=ACTIVE)
                BtnA9.config(state=ACTIVE)
            elif ItmNm10.get() == '':
                ItmNm10.set(i[2])
                MRP10var.set(i[5])
                Qty10.set(AddQty.get())
                Total10.set(int(MRP10var.get()) * int(Qty10.get()))
                BtnM10.config(state=ACTIVE)
                BtnA10.config(state=ACTIVE)
            else:
                messagebox.showerror('Error', 'Maximum 10 items allowed per billing.')
            FinlAmount.set('Total Amount: ' + str(
                int(MRP1var.get()) * int(Qty1.get()) + int(MRP2var.get()) * int(Qty2.get()) + int(MRP3var.get()) * int(
                    Qty3.get()) + int(MRP4var.get()) * int(Qty4.get()) + int(MRP5var.get()) * int(Qty5.get()) + int(
                    MRP6var.get()) * int(Qty6.get()) + int(MRP7var.get()) * int(Qty7.get()) + int(MRP8var.get()) * int(
                    Qty8.get()) + int(MRP9var.get()) * int(Qty9.get()) + int(MRP10var.get()) * int(Qty10.get())))
        txtItemRef.set('')
        AddQty.delete(0, END)
        displayStockView()
    except Exception:
        messagebox.showinfo('Information', 'No such reference number.')


def findproduct():
    ItemrefView.delete(0, END)
    ItemnameView.delete(0, END)
    ItemtypeView.delete(0, END)
    conn = sqlite3.connect('Grocery.db')
    cur = conn.cursor()
    sel = cur.execute(
        'SELECT ItemRef,ItemName,ItemType FROM StockDetails WHERE ItemName LIKE ? OR ItemRef LIKE ? OR ItemType LIKE ?',
        (
            '%{}%'.format(txtItemRef.get()), '%{}%'.format(txtItemRef.get()), '%{}%'.format(txtItemRef.get()),))
    index = 0
    for i in sel:
        ItemrefView.insert(index, i[0])
        ItemnameView.insert(index, i[1])
        ItemtypeView.insert(index, i[2])


def test(event):
    try:
        select = ItemrefView.curselection()[0]
        refvalue = ItemrefView.get(select)
        txtItemRef.set('')
        txtItemRef.set(refvalue)
    except Exception:
        pass


def scroll_view_stock_view(*args):
    lstBarcode.yview(*args)
    lstItemRef.yview(*args)
    lstItemName.yview(*args)
    lstItemType.yview(*args)
    lstQuantity.yview(*args)
    lstMRP.yview(*args)
    lstExpiry.yview(*args)





def StockView():
    global lstBarcode, lstItemRef, lstItemName, lstItemType, lstQuantity, lstMRP, lstExpiry
    frameStockData = Frame(root, bd=4, relief='raise')
    frameStockData.place(x=50, y=530)
    scrollbar = Scrollbar(frameStockData, command=scroll_view_stock_view)
    scrollbar.grid(row=1, column=7, sticky=N + S)
    lblBarcode = Label(frameStockData, text='Barcode')
    lblBarcode.grid(row=0, column=0)
    lstBarcode = Listbox(frameStockData, width=15, height=10, yscrollcommand=scrollbar.set)
    lstBarcode.grid(row=1, column=0)
    lblItemRef = Label(frameStockData, text='Item Ref')
    lblItemRef.grid(row=0, column=1)
    lstItemRef = Listbox(frameStockData, width=20, height=10, yscrollcommand=scrollbar.set)
    lstItemRef.grid(row=1, column=1)
    lblItemName = Label(frameStockData, text='Item Name')
    lblItemName.grid(row=0, column=2)
    lstItemName = Listbox(frameStockData, width=30, height=10, yscrollcommand=scrollbar.set)
    lstItemName.grid(row=1, column=2)
    lblItemType = Label(frameStockData, text='Item Type')
    lblItemType.grid(row=0, column=3)
    lstItemType = Listbox(frameStockData, width=20, height=10, yscrollcommand=scrollbar.set)
    lstItemType.grid(row=1, column=3)
    lblQuantity = Label(frameStockData, text='Stock')
    lblQuantity.grid(row=0, column=4)
    lstQuantity = Listbox(frameStockData, width=5, height=10, yscrollcommand=scrollbar.set)
    lstQuantity.grid(row=1, column=4)
    lblMRP = Label(frameStockData, text='M.R.P.')
    lblMRP.grid(row=0, column=5)
    lstMRP = Listbox(frameStockData, width=8, height=10, yscrollcommand=scrollbar.set)
    lstMRP.grid(row=1, column=5)
    lblExpiry = Label(frameStockData, text='Expiry Date')
    lblExpiry.grid(row=0, column=6)
    lstExpiry = Listbox(frameStockData, width=15, height=10, yscrollcommand=scrollbar.set)
    lstExpiry.grid(row=1, column=6)


def displayStockView():
    lstBarcode.delete(0, END)
    lstItemRef.delete(0, END)
    lstItemName.delete(0, END)
    lstItemType.delete(0, END)
    lstQuantity.delete(0, END)
    lstMRP.delete(0, END)
    lstExpiry.delete(0, END)
    index = 0
    for i in ObjViewStock.view():
        index += 1
        lstBarcode.insert(index, i[0])
        lstItemRef.insert(index, i[1])
        lstItemName.insert(index, i[2])
        lstItemType.insert(index, i[3])
        lstQuantity.insert(index, i[4])
        lstMRP.insert(index, i[5])
        lstExpiry.insert(index, i[6])


def resetfun(a, b):
    coll1 = a.execute('SELECT Stock,ItemName FROM StockDetails WHERE ItemName=?', (b,))
    for upd1 in coll1:
        lisy1 = upd1[0]
    lisy1 = int(lisy1)
    upd1 = int(Qty1.get())
    save1 = lisy1 + upd1
    a.execute('UPDATE StockDetails SET Stock=? WHERE ItemName=?', (save1, b,))
    ItmNm1.set('')
    MRP1var.set(0)
    Qty1.set(0)
    Total1.set('')


def reset():
    conn = sqlite3.connect('Grocery.db')
    cur = conn.cursor()
    if ItmNm1.get() != '':
        resetfun(cur, ItmNm1.get())
    if ItmNm2.get() != '':
        resetfun(cur, ItmNm2.get())
    if ItmNm3.get() != '':
        resetfun(cur, ItmNm3.get())
    if ItmNm4.get() != '':
        resetfun(cur, ItmNm4.get())
    if ItmNm5.get() != '':
        resetfun(cur, ItmNm5.get())
    if ItmNm6.get() != '':
        resetfun(cur, ItmNm6.get())
    if ItmNm7.get() != '':
        resetfun(cur, ItmNm7.get())
    if ItmNm8.get() != '':
        resetfun(cur, ItmNm8.get())
    if ItmNm9.get() != '':
        resetfun(cur, ItmNm9.get())
    if ItmNm10.get() != '':
        resetfun(cur, ItmNm10.get())
    FinlAmount.set('Total Amount: ')
    conn.commit()
    displayStockView()


def check():
    ObjViewStock.com()


def bill():
    BillEG.delete('1.0', END)
    if ItmNm1.get() != '' and len(CustName.get()) != 2 and len(CustMobile.get()) == 10:
        BillNum = random.randint(123456, 654321)
        BillRef = 'BILL' + str(BillNum)
        now = datetime.now()
        dt_string = now.strftime('%d/%b/%Y %H:%M:%S')

        for row in ObjViewStore.view():
            BillEG.insert(END, '\n\n\t\t' + row[0] + '\n')
            BillEG.insert(END, '\t' + row[1] + ',' + row[4] + ',' + row[5] + '\n\n')
            BillEG.insert(END, '\t================================\n\n')
            BillEG.insert(END, 'Email-ID: ' + row[2] + '\n')
            BillEG.insert(END, 'Contact Us at: ' + row[3] + '\n')
            BillEG.insert(END, '--------------------------------------------------\n')
            BillEG.insert(END, 'Bill No: ' + BillRef + '\n')
            BillEG.insert(END, 'Purchased on: ' + dt_string + '\n')
            BillEG.insert(END, '--------------------------------------------------')
            BillEG.insert(END, '\t\t\tCustomer Info\n')
            BillEG.insert(END, 'Name: ' + CustName.get() + '\n')
            BillEG.insert(END, 'Mobile: ' + CustMobile.get() + '\n')
            BillEG.insert(END, '--------------------------------------------------\n')
            BillEG.insert(END, 'Item Name\t\t\tQty\tRate\tNet Amt.\n')
            BillEG.insert(END, '--------------------------------------------------\n')
            if ItmNm1.get() != '' or len(ItmNm1.get()) > 23:
                BillEG.insert(END,
                              ItmNm1.get()[
                              0:23] + Qty1.get() + '\t' + MRP1var.get() + '\t' + Total1.get() + '\n' + ItmNm1.get()[
                                                                                                       23:] + '\n')
            if ItmNm2.get() != '' and len(ItmNm2.get()) > 23:
                BillEG.insert(END,
                              ItmNm2.get()[
                              0:23] + '\t\t\t' + Qty2.get() + '\t' + MRP2var.get() + '\t' + Total2.get() + '\n' + ItmNm2.get()[
                                                                                                                  23:] + '\n')
            if ItmNm3.get() != '' and len(ItmNm3.get()) > 23:
                BillEG.insert(END,
                              ItmNm3.get()[
                              0:23] + '\t\t\t' + Qty3.get() + '\t' + MRP3var.get() + '\t' + Total3.get() + '\n' + ItmNm3.get()[
                                                                                                                  23:] + '\n')
            if ItmNm4.get() != '' and len(ItmNm4.get()) > 23:
                BillEG.insert(END,
                              ItmNm4.get()[
                              0:23] + '\t\t\t' + Qty4.get() + '\t' + MRP4var.get() + '\t' + Total4.get() + '\n' + ItmNm4.get()[
                                                                                                                  23:] + '\n')
            if ItmNm5.get() != '' and len(ItmNm5.get()) > 23:
                BillEG.insert(END,
                              ItmNm5.get()[
                              0:23] + '\t\t\t' + Qty5.get() + '\t' + MRP5var.get() + '\t' + Total5.get() + '\n' + ItmNm5.get()[
                                                                                                                  23:] + '\n')
            if ItmNm6.get() != '' and len(ItmNm6.get()) > 23:
                BillEG.insert(END,
                              ItmNm6.get()[
                              0:23] + '\t\t\t' + Qty6.get() + '\t' + MRP6var.get() + '\t' + Total6.get() + '\n' + ItmNm6.get()[
                                                                                                                  23:] + '\n')
            if ItmNm7.get() != '' and len(ItmNm7.get()) > 23:
                BillEG.insert(END,
                              ItmNm7.get()[
                              0:23] + '\t\t\t' + Qty7.get() + '\t' + MRP7var.get() + '\t' + Total7.get() + '\n' + ItmNm7.get()[
                                                                                                                  23:] + '\n')
            if ItmNm8.get() != '' and len(ItmNm8.get()) > 23:
                BillEG.insert(END,
                              ItmNm8.get()[
                              0:23] + '\t\t\t' + Qty8.get() + '\t' + MRP8var.get() + '\t' + Total8.get() + '\n' + ItmNm8.get()[
                                                                                                                  23:] + '\n')
            if ItmNm9.get() != '' and len(ItmNm9.get()) > 23:
                BillEG.insert(END,
                              ItmNm9.get()[
                              0:23] + '\t\t\t' + Qty9.get() + '\t' + MRP9var.get() + '\t' + Total9.get() + '\n' + ItmNm9.get()[
                                                                                                                  23:] + '\n')
            if ItmNm10.get() != '' and len(ItmNm10.get()) > 23:
                BillEG.insert(END,
                              ItmNm10.get()[
                              0:23] + '\t\t\t' + Qty10.get() + '\t' + MRP10var.get() + '\t' + Total10.get() + '\n' + ItmNm10.get()[
                                                                                                                     23:] + '\n')
            BillEG.insert(END, '--------------------------------------------------\n')
            BillEG.insert(END, FinlAmount.get() + '\n')
            BillEG.insert(END, '--------------------------------------------------\n')
            BillEG.insert(END, '***This is a computer generated invoice. No signature is required.***')
            f1 = open(BillRef, 'w')
            f1.write(BillEG.get('1.0', 'end'))
            iPrint()
    else:
        messagebox.showerror('Error', 'Check if an Order is placed,Customer Info is correctly entered.')


def Play():
    global paused
    if paused:
        mixer.music.unpause()
        MusicStatus['text'] = 'Resumed Music!'
        paused = FALSE
    else:
        try:
            global play_it
            selected_song = MusicListBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            MusicStatus['text'] = 'Playing Music!' + '-' + os.path.basename(play_it)
        except:
            messagebox.showerror('Error', 'File not exists.')


paused = FALSE


def Pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    MusicStatus['text'] = 'Music Paused!'


def Stop():
    mixer.music.stop()
    MusicStatus['text'] = 'Music Stopped!'


def set_val(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def Mute():
    global muted
    if muted:
        mixer.music.set_volume(0.2)
        MuteBtn.configure(image=MuteButtonPhoto)
        volume.set(20)
        muted = FALSE
        MusicStatus['text'] = 'Music Unmuted!'
    else:
        mixer.music.set_volume(0)
        MuteBtn.configure(image=VolumeButtonPhoto)
        volume.set(0)
        muted = TRUE
        MusicStatus['text'] = 'Music Muted!'


playlist = []


def browse_music():
    global filename_path
    index = 0
    filename_path = filedialog.askopenfilename()
    filename = os.path.basename(filename_path)
    MusicListBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


def remove_music():
    selected_song = MusicListBox.curselection()
    selected_song = int(selected_song[0])
    MusicListBox.delete(selected_song)
    playlist.pop(selected_song)


SearchStockButtonPhoto = PhotoImage(file=r"images/SearchIcon.png")
SrchBtn = Button(root, text='Search', image=SearchStockButtonPhoto, command=findproduct)
SrchBtn.place(x=50, y=280)
ToolTipText.CreateToolTip(SrchBtn, 'Search')

GenBillButtonPhoto = PhotoImage(file=r"images/generateBill.png")
GenBillBtn = Button(root, text='Search', image=GenBillButtonPhoto, command=bill)
GenBillBtn.place(x=800, y=420)
ToolTipText.CreateToolTip(GenBillBtn, 'Generate Bill')

ResetBillButtonPhoto = PhotoImage(file=r"images/resetBill.png")
ResetBillBtn = Button(root, text='Search', image=ResetBillButtonPhoto, command=reset)
ResetBillBtn.place(x=800, y=520)
ToolTipText.CreateToolTip(ResetBillBtn, 'Reset Bill')

AddBillButtonPhoto = PhotoImage(file=r"images/addBill.png")
AddBtn = Button(root, text='Add Stock', image=AddBillButtonPhoto, command=addbill)
AddBtn.place(x=100, y=280)
ToolTipText.CreateToolTip(AddBtn, 'Add to Bill')

PlayButtonPhoto = PhotoImage(file=r"images/play.png")
PlayBtn = Button(root, text='Play', image=PlayButtonPhoto, command=Play)
PlayBtn.place(x=1100, y=80)
ToolTipText.CreateToolTip(PlayBtn, 'Play')

PauseButtonPhoto = PhotoImage(file=r"images/pause.png")
PauseBtn = Button(root, text='Pause', image=PauseButtonPhoto, command=Pause)
PauseBtn.place(x=1020, y=80)
ToolTipText.CreateToolTip(PauseBtn, 'Pause')

StopButtonPhoto = PhotoImage(file=r"images/stop.png")
StopBtn = Button(root, text='Stop', image=StopButtonPhoto, command=Stop)
StopBtn.place(x=1180, y=80)
ToolTipText.CreateToolTip(StopBtn, 'Stop')

MuteButtonPhoto = PhotoImage(file=r"images/mute.png")
VolumeButtonPhoto = PhotoImage(file=r'images/volume.png')
MuteBtn = Button(root, text='Mute', image=MuteButtonPhoto, command=Mute)
MuteBtn.place(x=1260, y=80)
ToolTipText.CreateToolTip(MuteBtn, 'Mute')

MusicListBox = Listbox(root, width=40)
MusicListBox.place(x=1020, y=150)
MusicListBox.bind('<<ListboxSelect>>', Play)

volume = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_val)
volume.set(20)
mixer.music.set_volume(0.2)
volume.place(x=1115, y=30)

AddFiles = Button(root, text='+', command=browse_music)
AddFiles.place(x=1300, y=150)

RemoveFiles = Button(root, text='-', command=remove_music)
RemoveFiles.place(x=1300, y=180)

MusicStatus = Label(root, text='Music Status Here!', anchor='c', font=('bold'), bg='#000000', foreground='white',
                    width=25)
MusicStatus.place(x=1050, y=10)

prolist()
StockView()
displayStockView()
design()
mainloop()
