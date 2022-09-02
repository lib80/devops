"""栈的应用之中缀表达式求值"""
from stack_v1 import Stack


optr_level = {'(': 1, '+': 2, '-': 2, '*': 3, '/': 3}


def do_math(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


def calculate(exp_str):
    opnd = Stack()
    optr = Stack()
    for i in exp_str:
        if i.isdigit():
            opnd.push(int(i))
        elif i == '(':
            optr.push(i)
        elif i == ')':
            while optr.top() != '(':
                op = optr.pop()
                op2 = opnd.pop()  # 注意：先弹出的是第2个操作数
                op1 = opnd.pop()
                res = do_math(op, op1, op2)
                opnd.push(res)
            else:
                optr.pop()
        else:
            while not optr.is_empty() and optr_level.get(i) <= optr_level.get(optr.top()):
                op = optr.pop()
                op2 = opnd.pop()
                op1 = opnd.pop()
                res = do_math(op, op1, op2)
                opnd.push(res)
            else:
                optr.push(i)

    while not optr.is_empty():
        op = optr.pop()
        op2 = opnd.pop()
        op1 = opnd.pop()
        res = do_math(op, op1, op2)
        opnd.push(res)

    return opnd.pop()


print(calculate('(3-5)*(6+17*4)/3'))
