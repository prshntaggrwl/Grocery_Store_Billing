import sqlite3
from tkinter import *


class Stock:
    def __init__(self):
        self.conn = sqlite3.connect('Grocery.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS StockDetails(Barcode TEXT NOT NULL UNIQUE,ItemRef TEXT,ItemName TEXT,ItemType TEXT,'
            'Stock TEXT, '
            'MRP TEXT,Expiry TEXT)')
        self.conn.commit()

    def insert(self, Barcode, ItemRef, ItemName, ItemType, Quantity, MRP, Expiry):
        self.cur.execute('INSERT INTO StockDetails VALUES(?,?,?,?,?,?,?)',
                         (Barcode, ItemRef, ItemName, ItemType, Quantity, MRP, Expiry))
        self.conn.commit()

    def update(self, txtItemRef, txtItemName, txtItemType, upd, MRP, txtExpiry):
        self.cur.execute(
            'UPDATE StockDetails SET ItemRef=?,ItemName=?,ItemType=?,Stock=?,MRP=?,Expiry=? WHERE ItemRef=?',
            (txtItemRef.get(), txtItemName.get(), txtItemType.get(), upd, MRP.get(), txtExpiry.get(), txtItemRef.get()))

    def view(self):
        self.cur.execute('SELECT * FROM StockDetails')
        row = self.cur.fetchall()
        return row

    def viewUpdItem(self, txtItemRef):
        sel = self.cur.execute('select * from StockDetails where ItemRef=?', txtItemRef,)
        return sel

    def modify(self, a):
        sel = self.cur.execute('SELECT Stock,ItemName FROM StockDetails WHERE ItemName=?', (a,))

    def modifyStock(self, upd, a):
        self.cur.execute('UPDATE StockDetails SET Stock=? WHERE ItemName=?', (upd, a))
        self.conn.commit()

    def com(self):
        self.conn.commit()

    def Search(self, optvar):
        self.cur.execute(
            'SELECT * FROM StockDetails WHERE ItemName LIKE ? OR Barcode LIKE ? OR ItemRef LIKE ? OR ItemType LIKE ?',
            ('%{}%'.format(optvar), '%{}%'.format(optvar), '%{}%'.format(optvar), '%{}%'.format(optvar),))
        row = self.cur.fetchall()
        return row

    def delete(self, z):
        self.cur.execute('DELETE FROM StockDetails WHERE ItemRef=?', (z,))
        self.conn.commit()

    def show(self,a):
        q = self.cur.execute('SELECT ItemName,MRP FROM StockDetails WHERE ItemRef=?',
                             (a.upper(),))
        row = self.cur.fetchall()
        return row

class UserData:
    def __init__(self):
        self.conn = sqlite3.connect('Grocery.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS UserData(id INTEGER PRIMARY KEY,Name TEXT,UserType TEXT,DoB TEXT,Qualification '
            'TEXT,Address TEXT, '
            'State TEXT,Pin TEXT,EMail TEXT UNIQUE,Password TEXT)')
        self.conn.commit()

    def insert(self, Name, UserType, Dob, Qualification, Address, State, Pin, Email, Password):
        self.cur.execute('INSERT INTO UserData VALUES(NULL,?,?,?,?,?,?,?,?,?)',
                         (Name, UserType, Dob, Qualification, Address, State, Pin, Email, Password))
        self.conn.commit()

    def view(self):
        self.cur.execute('SELECT * FROM UserData')
        row = self.cur.fetchall()
        return row

    def delete(self, id):
        self.cur.execute('DELETE FROM UserData WHERE id=?', (id,))
        self.conn.commit()

    def log(self, Email, Pass):
        self.cur.execute('SELECT * FROM UserData WHERE EMail=? AND Password=?', (Email, Pass))
        result = self.cur.fetchall()
        return result


class Store():
    def __init__(self):
        self.conn = sqlite3.connect('Grocery.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS StoreDetails(StoreName TEXT,Address TEXT,Email TEXT UNIQUE,Phone TEXT,State TEXT,Pin TEXT,Password TEXT)')
        self.conn.commit()

    def insert(self, StoreName, Address, Email, Phone, State, Pin, Password):
        self.cur.execute('INSERT INTO StoreDetails VALUES(?,?,?,?,?,?,?)',
                         (StoreName, Address, Email, Phone, State, Pin, Password))
        self.conn.commit()

    def view(self):
        self.cur.execute('SELECT * FROM StoreDetails')
        row = self.cur.fetchall()
        return row


class AvailableStockView():
    def __int__(self):
        pass

    def scroll_view(self,*args):
        lstBarcode.yview(*args)
        lstItemName.yview(*args)
        lstItemType.yview(*args)
        lstQuantity.yview(*args)
        lstMRP.yview(*args)
        lstExpiry.yview(*args)
        lstItemRef.yview(*args)

    def onmousewheel(self,event):
        lstBarcode.ywiew = ('scroll', event.delta, 'units')
        lstItemRef.ywiew = ('scroll', event.delta, 'units')
        lstItemName.ywiew = ('scroll', event.delta, 'units')
        lstItemType.ywiew = ('scroll', event.delta, 'units')
        lstQuantity.ywiew = ('scroll', event.delta, 'units')
        lstMRP.ywiew = ('scroll', event.delta, 'units')
        lstExpiry.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    def view(self, a, b, h, q):
        global lstBarcode, lstItemRef, lstItemName, lstItemType, lstQuantity, lstMRP, lstExpiry
        scrollbar = Scrollbar(a, command=b)
        scrollbar.grid(row=1, column=7, sticky=N + S)
        lblBarcode = Label(a, text='Barcode')
        lblBarcode.grid(row=0, column=0)
        lstBarcode = Listbox(a, width=15, height=h, yscrollcommand=scrollbar.set)
        lstBarcode.grid(row=1, column=0)
        lblItemRef = Label(a, text='Item Ref')
        lblItemRef.grid(row=0, column=1)
        lstItemRef = Listbox(a, width=20, height=h, yscrollcommand=scrollbar.set)
        lstItemRef.grid(row=1, column=1)
        lblItemName = Label(a, text='Item Name')
        lblItemName.grid(row=0, column=2)
        lstItemName = Listbox(a, width=30, height=h, yscrollcommand=scrollbar.set)
        lstItemName.grid(row=1, column=2)
        lblItemType = Label(a, text='Item Type')
        lblItemType.grid(row=0, column=3)
        lstItemType = Listbox(a, width=20, height=h, yscrollcommand=scrollbar.set)
        lstItemType.grid(row=1, column=3)
        lblQuantity = Label(a, text='Stock')
        lblQuantity.grid(row=0, column=4)
        lstQuantity = Listbox(a, width=5, height=h, yscrollcommand=scrollbar.set)
        lstQuantity.grid(row=1, column=4)
        lblMRP = Label(a, text='M.R.P.')
        lblMRP.grid(row=0, column=5)
        lstMRP = Listbox(a, width=8, height=h, yscrollcommand=scrollbar.set)
        lstMRP.grid(row=1, column=5)
        lblExpiry = Label(a, text='Expiry Date')
        lblExpiry.grid(row=0, column=6)
        lstExpiry = Listbox(a, width=15, height=h, yscrollcommand=scrollbar.set)
        lstExpiry.grid(row=1, column=6)
        lstBarcode.bind('<MouseWheel>', q)
        lstItemName.bind('<MouseWheel>', q)
        lstItemType.bind('<MouseWheel>', q)
        lstQuantity.bind('<MouseWheel>', q)
        lstMRP.bind('<MouseWheel>', q)
        lstExpiry.bind('<MouseWheel>', q)

    def display(self, z):
        lstBarcode.delete(0, END)
        lstItemRef.delete(0, END)
        lstItemName.delete(0, END)
        lstItemType.delete(0, END)
        lstQuantity.delete(0, END)
        lstMRP.delete(0, END)
        lstExpiry.delete(0, END)
        index = 0
        for i in z.view():
            index += 1
            lstBarcode.insert(index, i[0])
            lstItemRef.insert(index, i[1])
            lstItemName.insert(index, i[2])
            lstItemType.insert(index, i[3])
            lstQuantity.insert(index, i[4])
            lstMRP.insert(index, i[5])
            lstExpiry.insert(index, i[6])
