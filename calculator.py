import tkinter as tk
from tkinter import ttk
from tkinter.font import NORMAL

root = tk.Tk()
root.title('Calculator')
###root.geometry('300x300')
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

equation = ttk.Entry(root, width=54, state="readonly")
equation.grid(row=0, column=0, columnspan=9, padx=10, pady=10)

def buttonClick(str):
    print(str)
    equation.configure(state=NORMAL)
    if str == 'c':
        equation.delete(0,"end")
    else :
        equation.insert("end", str)
    equation.configure(state="readonly")

def addButton(value):
    return ttk.Button(root, text=value, width=6, command=lambda: buttonClick(str(value)),)

b0 = addButton(0)
b1 = addButton(1)
b2 = addButton(2)
b3 = addButton(3)
b4 = addButton(4)
b5 = addButton(5)
b6 = addButton(6)
b7 = addButton(7)
b8 = addButton(8)
b9 =  addButton(9)
b_add = addButton('+')
b_sub = addButton('-')
b_mult = addButton('*')
b_div = addButton('/')
b_exp = addButton('^')
b_sin = addButton('sin()')
b_cos = addButton('cos()')
b_tan = addButton('tan()')
b_cot = addButton('cot()')
b_ln = addButton('ln()')
b_log = addButton('log()')
b_paran1 = addButton('(')
b_paran2 = addButton(')')
b_brack1 = addButton('{')
b_brack2 = addButton('}')
b_point = addButton('.')
b_clear = addButton('c')
b_equal = addButton('=')

row1 = [b_paran2,b_sin,b_cos,b7,b8,b9,b_add]
row2 = [b_paran1, b_cot, b_tan, b4,b5,b6,b_sub]
row3 = [b_brack1, b_log, b_exp, b1,b2,b3,b_mult]
row4 = [b_brack2, b_ln, b_clear,b0,b_point, b_equal,b_div]

r = 1
for row in [row1, row2, row3, row4]:
    c = 0
    for button in row:
        button.grid(row=r, column=c, columnspan=1)
        c += 1
    r += 1



# start the app
root.mainloop()