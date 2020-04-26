from collections import deque
import time

class ProcessQueue(object):
    def __init__(self):
        self.queue = deque()
    def enqueue(self, func, *args):
        """ Add `func` to the internal queue.

        """
        self.queue.append((func, args))

    def dequeue(self):
        """ Pop the top function from the internal queue and call it.

        """
        if not self.queue:
            raise IndexError("The is not process in the queue")
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self,maxPeriod):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly.

        """
        start = time.clock()
        while self.queue and time.clock() - start < maxPeriod:
            self.dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """
        while self.queue:
            self.dequeue()
