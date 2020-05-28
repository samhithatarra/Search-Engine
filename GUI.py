# -- Sources Used -- 
# https://www.python-course.eu/tkinter_entry_widgets.php
# https://datatofish.com/entry-box-tkinter/ 
# ------------------

import tkinter as SearchEngine
import query
import tkinter as tk

#-------------
# Extra credit GUI implementation using tkinter 
#-------------

root= tk.Tk()
root.title("Search Engine")
canvas1 = tk.Canvas(root, width = 1300, height = 800)
canvas1.pack()

entry1 = tk.Entry (root, width = 100) 
canvas1.create_window(650, 100, window=entry1)
label1 = tk.Label(root, text= str(""))

#-------------
# Getting input from the entry widget and passing to our get_query
# function from query.py
# Then displaying the url results on the tkinter canvas 
#-------------
def getInput():  
    x1 = entry1.get()  
    counter1 = 650
    counter2 = 220
    label1 = tk.Label(root, text= str(""), width = 1300)
    canvas1.create_window(counter1, counter2, window=label1)
    label1.destroy()
   
    query_input = query.get_query(x1)
  
    query_ = query.extract_posting(query_input)

    label1 = tk.Label(root, text= str(query_), width = 1300)
    canvas1.create_window(counter1, counter2, window=label1)
       
    counter2 += 20

    
button1 = tk.Button(text='Enter a Query', command= getInput)
canvas1.create_window(650, 130, window=button1)

root.mainloop()