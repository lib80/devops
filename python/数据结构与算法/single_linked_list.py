class Node:
    """结点"""
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next_ = next_


class SingleLinkedList:
    """带头结点的单链表"""
    def __init__(self):
        self.head = Node(None)

    def append(self, elem):
        new_node = Node(elem)
        p = self.head
        while p.next_ is not None:
            p = p.next_
        p.next_ = new_node

    def prepend(self, elem):
        """头部插入"""
        new_node = Node(elem)
        new_node.next_ = self.head.next_
        self.head.next_ = new_node

    def insert(self, i, elem):
        new_node = Node(elem)
        p = self.head
        j = 0
        while p and j < i-1:
            p = p.next_
            j += 1
        if not p or j > i-1:  # 插入位置大于表长+1或者小于1，报错
            return 'error'
        new_node.next_ = p.next_
        p.next_ = new_node

    def is_empty(self):
        if self.head.next_:
            return False
        else:
            return True

    def length(self):
        p, count = self.head, 0
        while p.next_:
            count += 1
        return count

    def find(self, i):
        """查找第i个结点的值"""
        p, j = self.head.next_, 1
        while p and j < i:
            p = p.next_
            j += 1
        if not p or j > i:  # 如果i大于表长或小于1，则报错
            return 'error'
        else:
            return p.elem

    def index(self, elem):
        """按值查找，返回位置，查找失败返回0"""
        p, i = self.head.next_, 1
        while p and p.elem != elem:
            p = p.next_
            i += 1
        if p:
            return i
        else:
            return 0

    def remove(self, i):
        """删除第i个结点"""
        p, j = self.head.next_, 1
        while p and j < i-1:
            p = p.next_
            j += 1
        if not p or j > i-1:
            return 'error'
        else:
            q = p.next_
            p.next_ = q.next_
            del q
            return 'ok'

    def clear(self):
        """清空链表"""
        p = self.head.next_
        while p:
            q = p.next_
            del p
            p = q
        self.head.next_ = None
        return 'ok'

    def destroy(self):
        """销毁链表"""
        p = self.head
        while p:
            q = p.next_
            del p
            p = q
        self.head = None
        return 'ok'

    def printall(self):
        p = self.head.next_
        while p:
            print(p.elem)
            p = p.next_
