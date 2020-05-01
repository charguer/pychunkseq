#!/usr/bin/env python3

import stack
import chunk
import chunk_list
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
arg_seq = args.seq
chunk.set_capacity(args.chunk_capacity)
chunk_list.set_capacity(args.chunk_capacity)
"""stack.set_capacity(args.chunk_capacity)"""

t1 = time.time()

if arg_seq == "debug":
    q = seq.Seq()
    q.print_general(print_item)
    for i in range (R):
        for k in range(1, S):
            q.push_back(k)
            q.print_general(print_item)
        for _ in range(1, S):
            q.pop_back()
            q.print_general(print_item)

elif arg_seq == "chunk_stack":
    q = seq.Seq()
    for i in range(R):
        for k in range(1, S):
            q.push_back(k)
        for _ in range(1, S):
            q.pop_back()

elif arg_seq == "stdlib_back":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
        for k in range(1, S):
            x = stack_test.pop()
            #if (x != S+1-k):
             #,   exit()

elif arg_seq == "stdlib_front":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.insert(0, k)
        for k in range(1, S):
            x = stack_test.pop(0)
            #if (x != S+1-k):
             #,   exit()

elif arg_seq == "container_deque": # right
    deque_test = deque()

    for i in range(R):
        for k in range(1, S):
            deque_test.append(k)
        for _ in range(1, S):
            deque_test.pop()

elif arg_seq == "debug_stdlib":
    stack_test = []

    for i in range(R):
        for k in range(1, S):
            stack_test.append(k)
            print(stack_test)
        for _ in range(1, S):
            stack_test.pop()
            print(stack_test)

elif arg_seq == "debug_concat":
    s1 = seq.Seq()
    s2 = seq.Seq()
    for k in range(1, S):
        s1.push_back(k)
        s2.push_back(k + S - 1)
    s1.print_general(print_item)
    s2.print_general(print_item)
    s1.concat_back(s2)
    print("=== CONCAT ===")
    s1.print_general(print_item)

elif arg_seq == "concat_back":
    s1 = seq.Seq()
    s2 = seq.Seq()
    for k in range(1, S):
        s1.push_back(k)
        s2.push_back(k + S - 1)
    t1 = time.time()
    s1.concat_back(s2)

print("exectime", time.time() - t1)

