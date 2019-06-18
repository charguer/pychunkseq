#!/usr/bin/env python3

import stack
from collections import deque

N = 2 ** 12
S = 2 ** 4
q = stack.stack()

for i in range (N // S):
    for k in range(1, S):
        q.print_()
        q.push(k)
    q.print_()
    print()
    for _ in range(1, S):
        q.print_()
        q.pop()
    q.print_()
    print()

stack_test = []

for i in range(N // S):
    for k in range(1, S):
        stack_test.append(k)
    for _ in range(1, S):
        stack_test.pop()

deque_test = deque()

for i in range(N // S):
    for k in range(1, S):
        deque_test.append(k)
