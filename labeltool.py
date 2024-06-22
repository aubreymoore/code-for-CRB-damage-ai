import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3

conn = sqlite3.connect('/home/aubrey/Desktop/Guam07-training-set/code/mydb.db')
conn.row_factory = sqlite3.Row # enables getting results as a list of dicts 
cur = conn.cursor()
cur.execute('''select * from boxes
            order by conf ASC
            limit 5''')
rows = cur.fetchall()
conn.close()

for row in rows:
    print(dict(row))



   
i = 0
imax = len(rows) - 1
proc = None

def annotate(imagepath, proc):
    # proc = subprocess.run(
    #     ['python3', 
    #      '/home/aubrey/labelImg/labelImg.py', 
    #      imagepath]
    #     )
    if proc:
        proc.terminate()
    proc = subprocess.Popen(
        ['python3', 
         '/home/aubrey/labelImg/labelImg.py', 
         imagepath]
        )
    return proc

def first():
    global i
    i = 0
    txt_i = ttk.Label(master=window, text=i)
    txt_i.grid(row=2,column=4)
    update_and_annotate()

def previous():
    global i
    i = max(i-1, 0)
    txt_i = ttk.Label(master=window, text=i)
    txt_i.grid(row=2,column=4)
    update_and_annotate()
 
def next():
    global i
    i = min(i+1, imax)
    txt_i = ttk.Label(master=window, text=i)
    txt_i.grid(row=2,column=4)
    update_and_annotate()

def last():
    global i
    i = imax
    update_and_annotate()
       
def update_and_annotate(): 
    global proc   
    txt_i = ttk.Label(master=window, text=i)
    txt_i.grid(row=2,column=4)
    imagepath = rows[i]['imagepath']
    print('imagepath')
    proc = annotate(imagepath, proc)
 
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

window.mainloop()
