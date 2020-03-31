#!/usr/bin/env python3

import stack
import chunk
from collections import deque
import time
import argparse
import seq

parser = argparse.ArgumentParser()
parser.add_argument("-seq", type=str,
                    help="type of sequence", default="debug")
parser.add_argument("-n", type=int, help="total number of pushes", default=80)
parser.add_argument("-length", type=int, help="number of pushes in one cycle", default=80)
parser.add_argument("-chunk_capacity", type=int, help="capacity of the chunk", default=4) # 128 pour tests
args = parser.parse_args()

def print_item(item):
    print(item, end="")

global N, S, R

N = args.n
S = args.length
R = N // S
seq = args.seq
chunk.set_capacity(args.chunk_capacity)
"""stack.set_capacity(args.chunk_capacity)"""

t1 = time.time()

if seq == "debug":
    q = seq.Seq()
    q.print_general(print_item)
    for i in range (R):
        for k in range(1, S):
            q.push(k)
            q.print_general(print_item)
        print()
        for _ in range(1, S):
            q.pop_left()
            q.print_general(print_item)
        print()

elif seq == "chunk_stack":
    q = seq.Seq()
    for i in range(R):
        for k in range(1, S):
            q.push(k)
        for _ in range(1, S):
            q.pop_left()

elif seq == "stdlib_back":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
        for k in range(1, S):
            x = stack_test.pop()
            #if (x != S+1-k):
             #,   exit()

elif seq == "stdlib_front":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.insert(0, k)
        for k in range(1, S):
            x = stack_test.pop(0)
            #if (x != S+1-k):
             #,   exit()

elif seq == "container_deque": # right
    deque_test = deque()

    for i in range(R):
        for k in range(1, S):
            deque_test.append(k)
        for _ in range(1, S):
            deque_test.pop()

elif seq == "debug_stdlib":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
            print(stack_test)
        for _ in range(1, S):
            stack_test.pop()
            print(stack_test)

print("exectime", time.time() - t1)

