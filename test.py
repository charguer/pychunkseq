#!/usr/bin/env python3

import stack
import chunk
from collections import deque
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-seq", type=str,
                    help="type of sequence", default="debug")
parser.add_argument("-n", type=int, help="total number of pushes", default=80)
parser.add_argument("-length", type=int, help="number of pushes in one cycle", default=80)
parser.add_argument("-chunk_capacity", type=int, help="capacity of the chunk", default=4)
args = parser.parse_args()

global N, S, R

N = args.n
S = args.length
R = N // S
seq = args.seq
chunk.set_capacity(args.chunk_capacity)
"""stack.set_capacity(args.chunk_capacity)"""

t1 = time.time()

if seq == "debug":
    q = stack.stack()
    q.print_()
    for i in range (R):
        for k in range(1, S):
            q.push(k)
            q.print_()
        print()
        for _ in range(1, S):
            q.pop_left()
            q.print_()
        print()

elif seq == "chunk_stack":
    q = stack.stack()
    for i in range(R):
        for k in range(1, S):
            q.push(k)
        for _ in range(1, S):
            q.pop_left()

elif seq == "stdlib_list":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
        for k in range(1, S):
            x = stack_test.pop_left()
            #if (x != S+1-k):
             #,   exit()

elif seq == "container_deque":
    deque_test = deque()

    for i in range(R):
        for k in range(1, S):
            deque_test.append(k)
        for _ in range(1, S):
            deque_test.pop_left()

elif seq == "debug_stdlib":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
            print(stack_test)
        for _ in range(1, S):
            stack_test.pop_left()
            print(stack_test)

print("exectime", time.time() - t1)

