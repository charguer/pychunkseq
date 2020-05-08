import echunk
import view
FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

global K
K = 4

class Schunk:

    def __init__(self, support = echunk.Echunk(), view = view.View()):
        self.support = support
        self.view = view

    def is_empty(self):
        return self.view.seg_size == 0

    def is_full(self):
        return self.view.seg_size == K

    def push(self, pov, item):
        assert not self.is_full()
        if (self.is_aligned(pov)):
            new_support = self.support # if aligned we can use the same support
        else:
            new_support = self.support.ncopy(self.view)
        new_support.push(pov, item)
        if (pov == FRONT):
            new_head = (self.view.seg_head - 1) % K
        elif (pov == BACK):
            new_head = self.view.seg_head
        new_view = view.View(new_head, self.view.seg_size + 1)
        return Schunk(new_support, new_view)

    def is_aligned(self, pov):
        if (pov == FRONT):
            return self.support.head == self.view.seg_head and (not self.support.is_full())
        elif (pov == BACK):
            return ((self.view.seg_head + self.view.seg_size) % K) == ((self.support.head + self.support.size) % K) and (not self.support.is_full())

    def pop(self, pov):
        assert not self.is_empty()
        if (pov == FRONT):
            index = self.view.seg_head
            new_head = (self.view.seg_head + 1) % K
        elif (pov == BACK):
            index = (self.view.seg_head + self.view.seg_size - 1) % K
            new_head = self.view.seg_head
        element = self.support.get_absolute(index)
        new_view = view.View(new_head, self.view.seg_size - 1)
        return (Schunk(self.support, new_view), element)

    def print_general(self, print_item):
        self.support.print_view(self.view, print_item)

    def push_front(self, item):
        self.push(FRONT, item)

    def push_back(self, item):
        self.push(BACK, item)

    def pop_front(self):
        self.pop(FRONT)

    def pop_back(self):
        self.pop(BACK)
