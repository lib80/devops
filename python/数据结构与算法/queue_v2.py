"""队列的链表实现"""
class QNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next_ = next_


class LQueue:
    def __init__(self):
        self.head = QNode(None)
        self.front = self.head
        self.rear = self.head

    def is_empty(self):
        return self.front == self.rear

    def enqueue(self, e):
        new_node = QNode(e)
        self.rear.next_ = new_node
        self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            return 'The queue is empty.'
        else:
            d_node = self.front.next_
            e = d_node.elem
            self.front.next_ = d_node.next_
            if d_node == self.rear:
                self.rear = self.front
            del d_node
            return e

    def destroy(self):
        while self.front:
            p = self.front.next_
            del self.front
            self.front = p
        print('ok')

    def top(self):
        if self.is_empty():
            return 'error'
        else:
            return self.front.next_.elem
