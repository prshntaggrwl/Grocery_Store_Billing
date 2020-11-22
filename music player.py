import sqlite3
import openpyxl
from openpyxl import load_workbook
import re

def slugify(text, lower=1):
    if lower == 1:
        text = text.strip().lower()
    text = re.sub(r'[^\w _-]+', '', text)
    text = re.sub(r'[- ]+', '_', text)
    return text

#Replace with a database name
con = sqlite3.connect('test.db')
#replace with the complete path to youe excel workbook
wb = load_workbook(filename=r'StockDetails.xlsx')

sheets = wb.get_sheet_names()

for sheet in sheets:
    ws = wb[sheet]

    columns= []
    query = 'CREATE TABLE ' + str(slugify(sheet)) + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
    for row in next(ws.rows):
        query += ', ' + slugify(row.value) + ' TEXT'
        columns.append(slugify(row.value))
    query += ');'

    con.execute(query)

    tup = []
    for i, rows in enumerate(ws):
        tuprow = []
        if i == 0:
            continue
        for row in rows:
            tuprow.append(str(row.value).strip()) if str(row.value).strip() != 'None' else tuprow.append('')
        tup.append(tuple(tuprow))


    insQuery1 = 'INSERT INTO ' + str(slugify(sheet)) + '('
    insQuery2 = ''
    for col in columns:
        insQuery1 += col + ', '
        insQuery2 += '?, '
    insQuery1 = insQuery1[:-2] + ') VALUES('
    insQuery2 = insQuery2[:-2] + ')'
    insQuery = insQuery1 + insQuery2

    con.executemany(insQuery, tup)
    con.commit()

con.close()