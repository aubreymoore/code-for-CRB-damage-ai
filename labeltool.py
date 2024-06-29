import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3
from icecream import ic
import os

OBJECTS_DB_FILE_PATH = '/home/aubrey/Desktop/Guam07-training-set/code/rawdatasubset.sqlite3'
NEW_DATASET_DIR = '/home/aubrey/Desktop/Guam07-training-set/datasets/rawdatasubset'

def get_data():
    ic()
    sql = '''
    select rowid, * from detected_objects
    where subset != 'test' AND edited_flag = 0
    order by conf ASC
    LIMIT 50
    '''
    conn = sqlite3.connect(OBJECTS_DB_FILE_PATH)
    conn.row_factory = sqlite3.Row # get results as a list of dicts 
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def set_edited_flag(rowid):
    conn = sqlite3.connect(OBJECTS_DB_FILE_PATH)
    conn.execute(f'UPDATE detected_objects SET edited_flag = 1 WHERE rowid={rowid};')
    conn.commit()
    conn.close()
 
def annotate():
    global proc
    ic()
    ic(proc)
    if proc:
        ic('about to terminate proc')
        proc.terminate()
    subset = rows[i]['subset']
    filename = os.path.basename(rows[i]['imagepath'])
    imagepath = f'{NEW_DATASET_DIR}/{subset}/{filename}'
    ic(imagepath)
    proc = subprocess.Popen(['python3', '/home/aubrey/labelImg/labelImg.py', imagepath])
    ic(proc)
    set_edited_flag(rows[i]['rowid'])

# def update_and_annotate(i, proc): 
#     ic()
#     annotate()

def first():
    ic()
    global i
    i = 0
    add_info()
    
def previous():
    ic()
    global i
    i = max(i-1, 0)
    add_info()
    
def add_info():
    info = f'{i+1} of {imax+1}   xpos: {rows[i]["xpos"]}   conf: {rows[i]["conf"]:.2f}   cls: {rows[i]["cls"]}'
    txt_info = ttk.Label(master=window, text=info)
    txt_info.grid(row=3, column=0, columnspan=4)
    annotate()
    
def next():  
    ic()
    global i
    i = min(i+1, imax)
    add_info()
    
def last():
    ic()
    global i
    i = imax
    add_info()
       
# MAIN

# set up GUI
window = tk.Tk()
window.title('labeltool')
window.geometry('350x175')

btn_first = ttk.Button(master=window, text='first', command=first)
btn_first.grid(row=2, column=0)
btn_previous = ttk.Button(master=window, text='previous', command=previous)
btn_previous.grid(row=2, column=1)
btn_next = ttk.Button(master=window, text='next', command=next)
btn_next.grid(row=2, column=2)
btn_last = ttk.Button(master=window, text='last', command=last)
btn_last.grid(row=2, column=3)

# Initialize global variables
rows = get_data()
ic(rows[0]['imagepath'], rows[0]['subset'])

i = 0
imax = len(rows) - 1
proc = None
first()

# Start GUI
window.mainloop()
