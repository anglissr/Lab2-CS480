from cgi import test
from collections import namedtuple
from lib2to3.pgen2 import token
import math

OpInfo = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()

operators = ['+','-','*','/','^','(',')']
functions = {
    's' : "sin",
    'c' : "cos",
    't' : "tan",
    'o' : "cot",
    'l' : "log",
    'n' : "ln",
}

precedence = {
 '^': 4,
 '*': 3,
 '/': 3,
 '+': 2,
 '-': 2,
 '(': 9,
 ')': 0,
 'sin':0
 }


tokenized = []

def tokenize(equ):
    equ = equ.replace('sin', 's')
    equ = equ.replace('cos', 'c')
    equ = equ.replace('tan', 't')
    equ = equ.replace('cot', 'o')
    equ = equ.replace('log', 'l')
    equ = equ.replace('ln', 'n')
    print(equ)
    token = ''
    for i in range(len(equ)):
        #print(token)
        c = str(equ[i])
        print(c)
        #if c == '-':
        #    print(next.isdigit())
        #    if next.isdigit():
        #       token += c
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

def shuntingyard(tokens):
    queue = []
    opstack = []
    for t in tokens:
        #print(queue)
        #print(opstack)
        #print(t)
        
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
    return queue



def eval_postfix(tokens):

    stack = []

    for token in tokens:
        #print(token)
        
        if token.strip() == '':
            continue 

        elif token == "+":
            stack.append(stack.pop() + stack.pop())

        elif token == "-":
            op2 = stack.pop() 
            stack.append(stack.pop() - op2)

        elif token == '^':
            #print(stack[0])
            #print(stack[1])
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
        
        elif token == 'log':
            stack.append(math.log10(stack.pop()))

        elif token == '/':
            op2 = stack.pop()
            if op2 != 0.0:
                stack.append(stack.pop() / op2)
            else:
                raise ValueError("division by zero found!")

        elif (str(token).isnumeric or testFloat(token) ):
                stack.append(float(token))

        else:
            raise ValueError("unknown token {0}".format(token))
        #print(stack)
    if len(stack) > 1:
        raise Exception("Invalid format of equation")
    else:
        return stack.pop()


#equation1 = "-5.78+-(4-2.23)+sin(0) *cos (1)/(1+tan(2*ln(-3+2*(1.23+99.111))"
#equation = "200 cos(1-3)"
#equation2 = "3+4 + sin( 2^3 + 3 )"
#equation3 = "31 + 34"

#for i in tokenized:
    print(i, end =" ")
#print("")

#postfix = shuntingyard(tokenized)
#print(postfix)
#print(eval_postfix(postfix))


def calculate():
    tokenize(equation.get())
    eval_postfix(shuntingyard(tokenized))
    answer = str(eval(equation.get()))
    #print(answer)
    equation.delete(0, "end")
    equation.insert(0, answer)


