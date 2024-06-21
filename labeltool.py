import tkinter as tk
from tkinter import ttk
import subprocess

def annotate():
    subprocess.run(
        ['python3', 
         '/home/aubrey/labelImg/labelImg.py', 
         '/home/aubrey/Desktop/Guam07-training-set/datasets/test/train/IMG_20221115_112224.jpg']
        )
    
window = tk.Tk()
window.title('labeltool')
window.geometry('300x150')

button = ttk.Button(master=window, text='Annotate', command=annotate)
button.place(relx=0.5, rely=0.5, anchor='center')

window.mainloop()
