import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import math

operators = ['+','-','*','/','^','(',')']
operators2 = ['+','-','~','*','/','^','(']
functions = {
    's' : "sin",
    'c' : "cos",
    't' : "tan",
    'o' : "cot",
    'l' : "log",
    'n' : "ln",
    '~' : "~",
}

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



def convertUnaryMinus(tokenized):
    for i in (range(len(tokenized))):
        if i == 0 and tokenized[i] == '-':
            tokenized[i] = "~"
        else:
            if tokenized[i] == '-':
                if tokenized[i-1] in operators2:
                    tokenized[i] = "~"
    return tokenized

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
    print(equ)
    token = ''
    for i in range(len(equ)):
        #print(token)
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

def testFloat(t):
    try : 
        float(t)
        return True
    except :    
        return False

def peek(stack):
    return stack[-1] if stack else None

def greater_precedence(op1, op2):
    return precedence.get(op1) > precedence.get(op2)


# Shunting Yard Algorithm
# Adapted from https://rosettacode.org/wiki/Parsing/Shunting-yard_algorithm#Python
def shuntingyard(tokens):
    queue = []
    opstack = []
    for t in tokens:
        if str(t).isnumeric():
            queue.append(t)
        elif testFloat(t):
            queue.append(t)
        elif t in functions.values():
            opstack.append(t)
        elif str(t) == '(':
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
    print(queue)
    return queue


# Postfix notation evaluator
# Adapted from https://stackoverflow.com/questions/30067163/evaluating-postfix-in-python
def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token.strip() == '':
            continue 
        elif token == "+":
            stack.append(stack.pop() + stack.pop())

        elif token == "-":
            op2 = stack.pop() 
            stack.append(stack.pop() - op2)

        elif token == '^':
            power = stack.pop()
            base = stack.pop()
            stack.append(pow(base, power))

        elif token == '*':
            stack.append(stack.pop() * stack.pop())

        elif token == 'sin':
            stack.append(math.sin(stack.pop()))
        
        elif token == 'cos':
            stack.append(math.cos(stack.pop()))

        elif token == 'tan':
            stack.append(math.tan(stack.pop()))
        
        elif token == '~':
            stack.append(stack.pop() * -1 )
        
        elif token == 'log':
            stack.append(math.log10(stack.pop()))
        
        elif token == 'ln':
            stack.append(math.log(stack.pop()))

        elif token == '/':
            op2 = stack.pop()
            if op2 != 0.0:
                stack.append(stack.pop() / op2)
            else:
                raise ValueError("Divide by zero error")

        elif (str(token).isnumeric or testFloat(token) ):
                stack.append(float(token))

        else:
            raise ValueError("Unknown token {0}".format(token))
        print(stack)
    if len(stack) > 1:
        raise Exception("Invalid format of equation")
    else:
        return stack.pop()


#equation1 = "-5.78+-(4-2.23)+sin(0) *cos (1)/(1+tan(2*ln(-3+2*(1.23+99.111))"
#equation = "200 cos(1-3)"
#equation2 = "3+4 + sin( 2^3 + 3 )"
#equation3 = "31 + 34"

#for i in tokenized:
    #print(i, end =" ")
#print("")

#postfix = shuntingyard(tokenized)
#print(postfix)
#print(eval_postfix(postfix))


def calculate():
    if equation.get() != '':
        tokenized = tokenize(equation.get())
        print(tokenized)
        tokenized = convertUnaryMinus(tokenized)
        print(tokenized)
        answer = eval_postfix(shuntingyard(tokenized))
        if (float(answer).is_integer()):
            print(answer)
            answer = int(answer)
        #equation.configure(state=NORMAL)
        equation.delete(0, "end")
        equation.insert(0, answer)
        #equation.configure(state="readonly")

# Setup
root = tk.Tk()
root.title('Calculator')
root.resizable(False, False)
style = ttk.Style()
style.theme_use("clam")

# Create equeation entry box
equation = ttk.Entry(root, width=54)#, state="readonly")
equation.grid(row=0, column=0, columnspan=7, padx=10, pady=10)


# Detect the return key as "="
def equals(event):
    #print("You hit return.")
    
    calculate()

root.bind('<Return>', equals)


# Handleing tkinter button clicks
def buttonClick(str):
    #print(str)
    #equation.configure(state=NORMAL)
    if str == 'C':
        equation.delete(0,"end")
    elif str == '⌫':
        temp = equation.get()[:-1]
        equation.delete(0, "end")
        equation.insert(0, temp)
    elif str == '=':
        calculate()
    else :
        equation.insert("end", str)
    #equation.configure(state="readonly")



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
b_neg = ttk.Button(root, text="±", width=6, command=lambda: buttonClick(str("-")),)
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
b_equal = ttk.Button(root, text="=", width=15, command=lambda: buttonClick(str("=")),)
row1 = [b_paran2,b_sin,b_cos,b_backspace,b7,b8,b9,b_add]
row2 = [b_paran1, b_cot, b_tan,b_point,b4,b5,b6,b_sub]
row3 = [b_brack1, b_log, b_exp,b_neg, b1,b2,b3,b_mult]
row4 = [b_brack2, b_ln, b_clear,b_empty,b0,b_equal,b_div]

r = 2
for row in [row1, row2, row3, row4]:
    c = 0
    for button in row:
        button.grid(row=r, column=c, columnspan=1)
        c += 1
    r += 1

b_equal.grid_configure(columnspan=2,)
b_div.grid_configure(column=7)


# any name as accepted but not signature
def report_callback_exception(self, exc, val, tb):
    showerror("Error", message=str(val))
    #equation.configure(state="readonly")

tk.Tk.report_callback_exception = report_callback_exception
# now method is overridden

# start the app
root.mainloop()