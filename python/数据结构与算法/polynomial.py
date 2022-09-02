"""稀疏多项式相加：链表实现"""


class Node:
    """结点"""
    def __init__(self, coef, expn, next_=None):
        self.coef = coef
        self.expn = expn
        self.next_ = next_


class SingleLinkedList:
    """带头结点的单链表"""
    def __init__(self):
        self.head = Node(None, None)

    def append(self, coef, expn):
        new_node = Node(coef, expn)
        p = self.head
        while p.next_ is not None:
            p = p.next_
        p.next_ = new_node

    def prepend(self, coef, expn):
        """头部插入"""
        new_node = Node(coef, expn)
        new_node.next_ = self.head.next_
        self.head.next_ = new_node

    def insert(self, i, coef, expn):
        new_node = Node(coef, expn)
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
            return p.coef, p.expn

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
            print(p.coef, p.expn)
            p = p.next_


lla = SingleLinkedList()
llb = SingleLinkedList()
llc = SingleLinkedList()
for i in [(7, 0), (11, 1), (9, 8), (5, 17)]:
    lla.append(i[0], i[1])
for j in [(8, 1), (22, 7), (-9, 8)]:
    llb.append(j[0], j[1])

pa = lla.head.next_
pb = llb.head.next_
pc = llc.head = lla.head

while pa and pb:
    if pa.expn < pb.expn:
        pc.next_ = pa
        pc = pa
        pa = pa.next_
    elif pa.expn > pb.expn:
        pc.next_ = pb
        pc = pb
        pb = pb.next_
    else:
        if (pa.coef+pb.coef) != 0:
            pa.coef = pa.coef + pb.coef
            pc.next_ = pa
            pc = pa
        pa = pa.next_
        pb = pb.next_

if pa:
    pc.next_ = pa
else:
    pc.next_ = pb
del llb.head
