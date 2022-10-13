# Ryan Angliss
# Lab 2 CS 480
import tkinter as tk
from tkinter import ttk
from tkinter.font import NORMAL
from tkinter.messagebox import showerror
import math

# List of all possible operators/symbols
operators = ['+','-','*','/','^','(',')']
# List of all symbols that may come before a unary negation
operators2 = ['+','-','~','*','/','^','(']
# List of all functions with shortened symbol (one letter)
functions = {
    's' : "sin",
    'c' : "cos",
    't' : "tan",
    'o' : "cot",
    'l' : "log",
    'n' : "ln",
    '~' : "~",
}
# Precedence map for shunting yard algoritm
precedence = {
 '^': 4,
 '*': 3,
 '/': 3,
 '+': 2,
 '-': 2,
 '(': 9,
 ')': 0,
 'sin':0,
 'cos':0,
 'tan':0,
 'cot':0,
 'log':0,
 'ln':0,
 '~':8,
 }



# Function that iterates over the user submitted equation in tokenized form and converts all unary minus signs to a "~"
# so they can be more easily evaluated later
# Returns an edited list of all tokens
def convertUnaryMinus(tokens):
    for i in (range(len(tokens))):
        # Unary minus if it is at the begginning...
        if i == 0 and tokens[i] == '-':
            tokens[i] = "~"
        else:
            # or if it is after an operator
            if tokens[i] == '-':
                if tokens[i-1] in operators2:
                    tokens[i] = "~"
    return tokens



# Tokenize a user submitted equation. Returns a list with each unique operator/value
# Returns a list of all tokens in the given string equation
def tokenize(equ):
    tokenized = []
    equ = equ.replace('sin', 's')
    equ = equ.replace('cos', 'c')
    equ = equ.replace('tan', 't')
    equ = equ.replace('cot', 'o')
    equ = equ.replace('log', 'l')
    equ = equ.replace('ln', 'n')
    equ = equ.replace('}', ')')
    equ = equ.replace('{', '(')
    token = ''
    # Iterate over each character
    for i in range(len(equ)):
        c = str(equ[i])
        if c.isdigit():
            token += c
        elif c == '.':
            token += c    
        elif c in operators:
            if (token != ''):
                tokenized.append(token)
            tokenized.append(c)
            token = ''
        elif c in functions:
            if (token != ''):
                tokenized.append(token)
            tokenized.append(functions.get(c))
            token = ''
    if (token != ''):
        tokenized.append(token)
    return tokenized



# Shunting Yard helper functions
# Test if a value is a float
def testFloat(t):
    try : 
        float(t)
        return True
    except : 
        return False

# "Peek" function implemented for a python list
def peek(stack):
    return stack[-1] if stack else None

# Function that helps determine which out of two operaters has a higher precedence
def greater_precedence(op1, op2):
    return precedence.get(op1) > precedence.get(op2)

# Shunting Yard Algorithm
# Adapted from https://rosettacode.org/wiki/Parsing/Shunting-yard_algorithm#Python
def shuntingyard(tokens):
    queue = []
    opstack = []
    # Iterate over each token of the equation
    for t in tokens:
        if str(t).isnumeric(): # add integers to the queue
            queue.append(t)
        elif testFloat(t): # add floats to the queue
            queue.append(t)
        elif t in functions.values(): # add functions to the stack
            opstack.append(t)
        elif str(t) == '(': # add open parenthesis to the stack
            opstack.append(t)
        elif t == ')':
            top = peek(opstack)
            while top is not None and top != '(':
                operator = opstack.pop()
                queue.append(operator)
                top = peek(opstack)
            opstack.pop() # Discard the '('
            top = peek(opstack)
            if top in functions.values():
                operator = opstack.pop()
                queue.append(operator)
        elif t in operators:
            top = peek(opstack)
            while top is not None and top not in "()" and greater_precedence(top, t):
                operator = opstack.pop()
                queue.append(operator)
                top = peek(opstack)
            opstack.append(t)
    while peek(opstack) is not None:
        operator = opstack.pop()
        queue.append(operator)
    return queue


# Postfix notation evaluator
# Adapted from https://stackoverflow.com/questions/30067163/evaluating-postfix-in-python
def eval_postfix(tokens):
    stack = []
    # Iterate over each token, determine how to handle operators/functions
    for t in tokens:
        if t.strip() == '':
            continue 
        elif t == "+":
            stack.append(stack.pop() + stack.pop())
        elif t == "-":
            op2 = stack.pop() 
            stack.append(stack.pop() - op2)
        elif t == '^':
            power = stack.pop()
            base = stack.pop()
            stack.append(pow(base, power))
        elif t == '*':
            stack.append(stack.pop() * stack.pop())
        elif t == 'sin':
            stack.append(math.sin(stack.pop()))
        elif t == 'cos':
            stack.append(math.cos(stack.pop()))
        elif t == 'tan':
            stack.append(math.tan(stack.pop()))
        elif t == 'cot':
            stack.append(1/math.tan(stack.pop()))
        elif t == '~':
            stack.append(stack.pop() * -1 )
        elif t == 'log':
            stack.append(math.log10(stack.pop()))
        elif t == 'ln':
            stack.append(math.log(stack.pop()))
        elif t == '/':
            op2 = stack.pop()
            if op2 != 0.0: # Catch divide by zero errors
                stack.append(stack.pop() / op2)
            else:
                raise ValueError("Divide by zero error")
        elif (str(t).isnumeric() or testFloat(t)):
                stack.append(float(t))
        else:
            raise ValueError("Unknown token {0}".format(t))
        
    if len(stack) > 1:
        raise Exception("Invalid format of equation")
    else:
        return stack.pop()


# Main Calculation function
# Tokenizes equations, runs shunting yard and evaluation, and outputs to the gui
def calculate():
    if equation.get() != '':
        tokenized = tokenize(equation.get()) # Tokenize equation
        tokenized = convertUnaryMinus(tokenized) # Convert unary minus signs to "~" for easier calculations
        postfixNotation = shuntingyard(tokenized) # Run shunting-yard to get postfix notation
        answer = eval_postfix(postfixNotation) # Evaluate postfix to get answer
        # Print integer only if the answer is an int
        if (float(answer).is_integer()):
            answer = int(answer)

        # Write the the equation line on gui
        equation.configure(state=NORMAL)
        equation.delete(0, "end")
        equation.insert(0, answer)
        equation.configure(state="readonly")



# Tkinter Setup
root = tk.Tk()
root.title('Calculator')
root.resizable(False, False)
style = ttk.Style()
style.theme_use("alt")

# Create equation entry box
equation = ttk.Entry(root, width=55, state="readonly")
equation.grid(row=0, column=0, columnspan=8, padx=10, pady=10)

# Detect the return key as "="
def equals(event):
    calculate()
root.bind('<Return>', equals)

# Handleing tkinter button clicks
def buttonClick(str):
    equation.configure(state=NORMAL)
    if str == 'C': # Clear
        equation.delete(0,"end")
    elif str == '⌫': # Backspace
        temp = equation.get()[:-1]
        equation.delete(0, "end")
        equation.insert(0, temp)
    elif str == '=': # Equals
        calculate()
    else :
        equation.insert("end", str)
    equation.configure(state="readonly")

# Creating Tkinter UI
# Adapted from https://pyshark.com/basic-gui-calculator-in-python/
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
b_backspace = addButton('⌫')
b_mult = addButton('*')
b_div = addButton('/')
b_exp = addButton('^')
b_sin = ttk.Button(root, text="sin()", width=6, command=lambda: buttonClick(str("sin(")),)
b_cos = ttk.Button(root, text="cos()", width=6, command=lambda: buttonClick(str("cos(")),)
b_tan = ttk.Button(root, text="tan()", width=6, command=lambda: buttonClick(str("tan(")),)
b_cot = ttk.Button(root, text="cot()", width=6, command=lambda: buttonClick(str("cot(")),)
b_ln = ttk.Button(root, text="ln()", width=6, command=lambda: buttonClick(str("ln(")),)
b_log = ttk.Button(root, text="log()", width=6, command=lambda: buttonClick(str("log(")),)
b_paran1 = addButton('(')
b_paran2 = addButton(')')
b_brack1 = addButton('{')
b_brack2 = addButton('}')
b_point = addButton('.')
b_clear = addButton('C')
b_empty = addButton('')
b_empty1 = addButton('')
b_equal = ttk.Button(root, text="=", width=14, command=lambda: buttonClick(str("=")),)
row1 = [b_empty1,b_sin,b_cos,b_backspace,b7,b8,b9,b_add]
row2 = [b_empty, b_cot, b_tan,b_point,b4,b5,b6,b_sub]
row3 = [b_paran1, b_paran2,b_log, b_exp, b1,b2,b3,b_mult]
row4 = [b_brack1, b_brack2,b_ln, b_clear,b0,b_equal,b_div]

# Button layout
r = 2
for row in [row1, row2, row3, row4]:
    c = 0
    for button in row:
        button.grid(row=r, column=c, columnspan=1)
        c += 1
    r += 1
b_equal.grid_configure(columnspan=2)
b_div.grid_configure(column=7)


# Tkinter error handling and error popup gui
def report_callback_exception(self, exc, val, tb):
    if str(val) == "pop from empty list":
        showerror("Error", message="Invalid format of equation")
    else:
       showerror("Error", message=str(val)) 
    equation.configure(state="readonly")
tk.Tk.report_callback_exception = report_callback_exception


# start the app
root.mainloop()