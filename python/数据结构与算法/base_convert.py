"""栈的应用之进制转换"""
from basic import Stack


def convert(number, base):
    digits = '0123456789abcdef'
    dividend = number
    s = Stack()
    while dividend > 0:
        s.push(dividend % base)
        dividend //= base

    res = ''
    while not s.is_empty():
        res += digits[s.pop()]
    return res


print(convert(31, 16))
