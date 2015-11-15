from asyncio import PriorityQueue 

class TupleSortingOn0(tuple):
    def __lt__(self, rhs):
        return self[0] < rhs[0]
    def __gt__(self, rhs):
        return self[0] > rhs[0]
    def __le__(self, rhs):
        return self[0] <= rhs[0]
    def __ge__(self, rhs):
        return self[0] >= rhs[0]

class EventManager:
    queue = PriorityQueue()
    
    def __init_(self):
        pass

    def addevent(self, tick, function, data=None):
        if (data == None):
            self.queue.put_nowait(TupleSortingOn0((tick, function)))
        else:
            self.queue.put_nowait(TupleSortingOn0((tick, function, data)))
            
    def getevent(self):
        if self.queue.empty():
            return None

        return self.queue.get_nowait()
