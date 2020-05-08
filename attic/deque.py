import chunk
import random
from math import *

global K

def set_capacity(chunk_capacity):
    global K
    K = chunk_capacity

set_capacity(4)

class deque:

    def __init__(self):
        self.right = chunk.chunk()
        self.left = chunk.chunk()
        self.middle = None

    def push_right(self, item):
        if self.right.is_full():
            if self.middle == None:
                self.middle = deque()
            self.middle.push_right(self.right)
            self.right = chunk.chunk()
        self.right.push_back(item)

    def push_left(self, item):
        if self.left.is_full():
            if self.middle == None:
                self.middle = deque()
            self.middle.push_left(self.left)
            self.left = chunk.chunk()
        self.left.push_front(item)

    def pop_right(self):
        if self.right.is_empty():
            if self.middle != None and not self.middle.is_empty():
                self.right = self.middle.pop_right()
            elif not self.left.is_empty():
                return self.left.pop('back')
            else:
                raise IndexError("pop on empty")
        x = self.right.pop('back')

        if self.right.is_empty() and self.middle != None and not self.middle.is_empty():
            self.right = self.middle.pop_right()
        return x

    def pop_left(self):
        if self.left.is_empty():
            if self.middle != None and not self.middle.is_empty():
                self.left = self.middle.pop_left()
            elif not self.right.is_empty():
                return self.right.pop('front')
            else:
                raise IndexError("pop on empty")
        x = self.left.pop('front')
        if self.left.is_empty() and self.middle != None and not self.middle.is_empty():
            self.left = self.middle.pop_left()
        return x

    def is_empty(self):
        return self.left.is_empty() and self.right.is_empty() # and self.middle.is_empty()

    def top_right(self):
        i = self.nb_middle - 1
        return self.middle.head

    def top_left(self):
        i = 0
        return self.middle[i]

    def print_general(self, print_item):
        def f(c):
            c.print_general(print_item)
            print(" | ", end = "")
        self.left.print_general(print_item)
        if self.middle != None:
            self.middle.print_general(f)
            #print()
        self.right.print_general(print_item)

    def size(self):
        if self.middle != None:
            return (K * self.middle.size()) + self.right.size + self.left.size
        else:
            return self.right.size + self.left.size

    def print_(self):
        def f(x):
            print(x, end = "")
        self.print_general(f)
        print("\n=====================")

test_deque = deque()
maxi = 0
nb = 0
for i in range(40000):
    if test_deque.is_empty():
        nb_choices = 2
    else:
        nb_choices = 4
    nb = random.randint(1, nb_choices)
    if nb == 1:
        test_deque.push_right(i + 1)
    elif nb == 2:
        test_deque.push_left(i + 1)
    elif nb == 3:
        test_deque.pop_left()
    else:
        test_deque.pop_right()
    #test_deque.print_()
    if test_deque.size() > maxi:
        maxi = test_deque.size()
    if test_deque.size() > sqrt(40000):
        nb += 1
    #print(test_deque.size())

print("racine de n =", maxi)
print("k =", nb)
