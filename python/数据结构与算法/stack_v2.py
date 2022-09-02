"""栈的链表实现"""


class Node:
    """结点"""
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next_ = next_


class Stack:
    def __init__(self):
        self._top = None

    def is_empty(self):
        return self._top is None

    def top(self):
        if self._top:
            return self._top.elem
        else:
            return 'Error. The stack is empty.'

    def push(self, elem):
        self._top = Node(elem, self._top)

    def pop(self):
        if self._top:
            p = self._top
            self._top = self._top.next_
            return p.elem
        else:
            return 'Error. The stack is empty.'
