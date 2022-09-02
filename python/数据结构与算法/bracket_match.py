"""栈的应用之简单括号匹配"""
from basic import Stack


def match(open, close):
    opens = '{[('
    closes = '}])'
    return opens.index(open) == closes.index(close)


def par_checker(symbol_str):
    s = Stack()
    for symbol in symbol_str:
        if symbol in '{[(':
            s.push(symbol)
        else:
            if s.is_empty():
                return False
            else:
                if not match(s.pop(), symbol):
                    return False

    if s.is_empty():
        return True
    else:
        return False


print(par_checker('{()[(])}'))
