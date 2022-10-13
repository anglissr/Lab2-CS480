# Ryan Angliss
# Lab 2 CS 480
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.font import NORMAL

import math

# List of all possible operators/symbols
operators = ['+','-','*','/','^','(',')']
# List of all functions
functions =["sin","cos","tan","cot","log","ln","~"]
# List of all symbols that may come before a unary negation
unaryNegationOperators = ['+','-','~','*','/','^','(']
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



# Tokenize a given string that reresents an equation
#
# Input: a user created mathmatical equation as a str
# Returns: a tokenized list that represents the equation
def createTokenizedList(equation):
    tokenList = []
    token = ''
    # Iterate over each character
    for i in range(len(equation)):
        char = str(equation[i])
        # if the character is a digit or decimal, add it to the token
        if char.isdigit() or char == '.':
            token += char    
        
        # if the character is an operator, check if there is a token to add, then add the operator to the list
        elif char in operators:
            if (token != ''):
                tokenList.append(token)
            tokenList.append(char)
            token = ''

        # if the character is a letter, check if it is part of a function, then add that to the list
        elif char.isalpha():
            if str(equation[i:i+3]) in functions:
                if (token != ''):
                    tokenList.append(token)
                tokenList.append(str(equation[i:i+3]))
                token = ''
            if str(equation[i:i+2]) in functions:
                if (token != ''):
                    tokenList.append(token)
                tokenList.append(str(equation[i:i+2]))
                token = ''

    # Add the last token to the list, if any
    if (token != ''):
        tokenList.append(token)
    return tokenList



# Function that iterates over the user submitted equation in tokenized form and converts all unary minus signs to a "~"
#
# Input: a tokenized list that represents the equation
# Returns: a tokenized list with all unary minus signs changed to "~"
def convertMinusSigns(tokenList):
    for i in (range(len(tokenList))):
        # if there is a minus sign the begginning..
        if i == 0 and tokenList[i] == '-':
            tokenList[i] = "~"
        else:
            # or if it is after an operator
            if tokenList[i] == '-':
                if tokenList[i-1] in unaryNegationOperators:
                    tokenList[i-1] = "~"
    return tokenList



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
def greaterPrecedence(op1, op2):
    return precedence.get(op1) > precedence.get(op2)

# Shunting Yard Algorithm
# Adapted from https://rosettacode.org/wiki/Parsing/Shunting-yard_algorithm#Python
#
# Input: a tokenized list that represents the equation
# Returns: a list in postfix notation that represents the equation
def shuntingYardAlgorithm(tokenList):
    s = []
    q = []

    # Iterate over each token of the equation
    for t in tokenList:
        # add integers to the queue
        if str(t).isnumeric():
            q.append(t)
        # add floats to the queue
        elif testFloat(t): 
            q.append(t)
        # add functions to the stack
        elif t in functions: 
            s.append(t)
        # add open parenthesis to the stack
        elif str(t) == '(': 
            s.append(t)
        elif t == ')':
            top = peek(s)
            while top is not None and top != '(':
                operator = s.pop()
                q.append(operator)
                top = peek(s)
            s.pop() # Discard the '('
            top = peek(s)
            if top in functions:
                operator = s.pop()
                q.append(operator)
        elif t in operators:
            top = peek(s)
            while top is not None and top not in "()" and greaterPrecedence(top, t):
                operator = s.pop()
                q.append(operator)
                top = peek(s)
            s.append(t)
    while peek(s) is not None:
        operator = s.pop()
        q.append(operator)
    return q



# Postfix notation evaluator
# Adapted from https://stackoverflow.com/questions/30067163/evaluating-postfix-in-python
#
# Input: a list in postfix notation that represents the equation
# Returns: 
def evaluatePostfix(tokens):
    s = []
    # Iterate over each token, determine how to handle operators/functions
    for t in tokens:
        if t.strip() == '':
            continue 
        elif t == "+":
            s.append(s.pop() + s.pop())
        elif t == "-":
            op2 = s.pop() 
            s.append(s.pop() - op2)
        elif t == '^':
            power = s.pop()
            base = s.pop()
            s.append(pow(base, power))
        elif t == 'log':
            s.append(math.log10(s.pop()))
        elif t == 'ln':
            s.append(math.log(s.pop()))
        elif t == '*':
            s.append(s.pop() * s.pop())
        elif t == 'sin':
            s.append(math.sin(s.pop()))
        elif t == 'cos':
            s.append(math.cos(s.pop()))
        elif t == 'tan':
            s.append(math.tan(s.pop()))
        elif t == 'cot':
            s.append(1/math.tan(s.pop()))
        elif t == '~':
            s.append(s.pop() * -1 )
        elif t == '/':
            op2 = s.pop()
            if op2 != 0.0: # Catch divide by zero errors
                s.append(s.pop() / op2)
            else:
                raise ValueError("Divide by zero error")
        elif (str(t).isnumeric() or testFloat(t)):
                s.append(float(t))
        else:
            raise ValueError("Unknown token error: {0}".format(t))
        
    if len(s) > 1:
        raise Exception("Invalid equation format error")
    else:
        return s.pop()


# Main Calculation function
def calculate():
    # If field is not empty
    if equationFeild.get() != '':
        tokenList = createTokenizedList(equationFeild.get()) # Tokenize equation
        tokenList = convertMinusSigns(tokenList) # Convert unary minus signs to "~" for easier calculations
        postfix = shuntingYardAlgorithm(tokenList) # Run shunting-yard to get postfix notation
        answer = evaluatePostfix(postfix) # Evaluate postfix to get answer
        
        # Print integer only if the answer is an int
        if (float(answer).is_integer()):
            answer = int(answer)

        # Write the the equation line on gui
        equationFeild.configure(state=NORMAL)
        equationFeild.delete(0, "end")
        equationFeild.insert(0, answer)
        equationFeild.configure(state="readonly")



# Tkinter Setup
root = tk.Tk()
root.resizable(False, False)
root.title('CS 480 Calculator')
style = ttk.Style()
style.theme_use("alt")

# Create equation entry box
equationFeild = ttk.Entry(root, width=70, state="readonly")
equationFeild.grid(row=0, column=0, columnspan=8, padx=5, pady=5)

# Detect the return key as "="
def equals(event):
    calculate()
root.bind('<Return>', equals)

# Handleing tkinter button clicks
def buttonClick(str):
    equationFeild.configure(state=NORMAL)
    if str == 'C': # Clear
        equationFeild.delete(0,"end")
    elif str == '⌫': # Backspace
        temp = equationFeild.get()[:-1]
        equationFeild.delete(0, "end")
        equationFeild.insert(0, temp)
    elif str == '=': # Equals
        calculate()
    else :
        equationFeild.insert("end", str)
    equationFeild.configure(state="readonly")

# Creating Tkinter UI
# Adapted from https://pyshark.com/basic-gui-calculator-in-python/
style = ttk.Style()
style.configure("Custom.TButton",font="Arial 12",background="white")
def addButton(value):
    return ttk.Button(root, text=value, width=6,style="Custom.TButton", command=lambda: buttonClick(str(value)),)
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
b_back = addButton('⌫')
b_mult = addButton('*')
b_div = addButton('/')
b_exp = addButton('^')
b_paran1 = addButton('(')
b_paran2 = addButton(')')
b_brack1 = addButton('{')
b_brack2 = addButton('}')
b_point = addButton('.')
b_clear = addButton('C')
b_empty = addButton('')
b_empty1 = addButton('')
b_sin = ttk.Button(root, text="sin()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("sin(")),)
b_cos = ttk.Button(root, text="cos()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("cos(")),)
b_tan = ttk.Button(root, text="tan()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("tan(")),)
b_cot = ttk.Button(root, text="cot()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("cot(")),)
b_ln = ttk.Button(root, text="ln()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("ln(")),)
b_log = ttk.Button(root, text="log()", width=6,style="Custom.TButton", command=lambda: buttonClick(str("log(")),)
b_equal = ttk.Button(root, text="=", width=13,style="Custom.TButton", command=lambda: buttonClick(str("=")),)

# Button layout
row1 = [b_empty1,b_sin,b_cos,b_point,b7,b8,b9,b_add]
row2 = [b_empty, b_cot, b_tan,b_exp,b4,b5,b6,b_sub]
row3 = [b_paran1, b_paran2,b_log,b_back , b1,b2,b3,b_mult]
row4 = [b_brack1, b_brack2,b_ln, b_clear,b_equal,b0,b_div]
r = 2
for row in [row1, row2, row3, row4]:
    c = 0
    for button in row:
        button.grid(row=r, column=c, columnspan=1)
        c += 1
    r += 1
b_equal.grid_configure(columnspan=2)
b0.grid_configure(column=6)
b_div.grid_configure(column=7)


# Tkinter error handling and error popup gui
def report_callback_exception(self, exc, val, tb):
    if str(val) == "pop from empty list":
        showerror("Error", message="Invalid equation format error")
    else:
       showerror("Error", message=str(val)) 
    equationFeild.configure(state="readonly")
tk.Tk.report_callback_exception = report_callback_exception


# start the app
root.mainloop()