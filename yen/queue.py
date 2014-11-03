class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.insert(0, item)

    def enqueue_list(self, item_list):
        for item in item_list:
            self.enqueue(item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Task(object):
    def __init__(self, action, quantity):
        self.action = action
        self.quantity = quantity


