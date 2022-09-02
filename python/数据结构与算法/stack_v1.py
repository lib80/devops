"""栈的顺序表实现"""


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, elem):
        self.items.append(elem)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]

    def size(self):
        return self.items.__len__()

    def clear(self):
        while self.items:
            self.items.pop()
