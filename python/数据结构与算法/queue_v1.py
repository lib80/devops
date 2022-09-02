"""循环队列的顺序表实现"""
class SQueue:
    def __init__(self, size=6):
        self.size = size
        self.queue = [None] * size
        self.front = 0
        self.rear = 0

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return self.front == ((self.rear + 1) % self.size)

    def enqueue(self, e):
        if self.is_full():
            print('The queue is full.')
        else:
            self.queue[self.rear] = e
            self.rear = (self.rear + 1) % self.size

    def dequeue(self):
        if self.is_empty():
            return 'The queue is empty.'
        else:
            e = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return e
