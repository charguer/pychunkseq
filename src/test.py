#!/usr/bin/env python3

import echunk
from collections import deque
import time
import argparse
from esek import Esek

parser = argparse.ArgumentParser()
parser.add_argument("-test", type=str,
                    help="type of test", default="stack")
parser.add_argument("-seq", type=str,
                    help="type of sequence", default="debug")
parser.add_argument("-n", type=int, help="total number of pushes", default=80)
parser.add_argument("-length", type=int, help="length of the sequence manipulated", default=80)
parser.add_argument("-chunk_capacity", type=int, help="capacity of the chunk", default=4) # 128 pour tests
args = parser.parse_args()

def print_item(item):
    print(item, end="")

global N, S, R

N = args.n
S = args.length

if N % S != 0:
    raise ValueError("Invalid values: 'n' must be divisible by 'length'")

R = N // S
arg_test = args.test
arg_seq = args.seq
echunk.set_capacity(args.chunk_capacity)
"""stack.set_capacity(args.chunk_capacity)"""

t1 = time.time()
tminus = 0
s = 0

if arg_test == "stack":
   if arg_seq == "debug":
       q = Esek.create_empty()
       q.print_general(print_item)
       for i in range (R):
           for k in range(1, S):
               q.push_back(k)
               q.print_general(print_item)
           for _ in range(1, S):
               q.pop_back()
               q.print_general(print_item)

   elif arg_seq == "esek_back":
       q = Esek.create_empty()
       for i in range(R):
           for k in range(1, S):
               q.push_back(k)
           for _ in range(1, S):
               s += q.pop_back()

   elif arg_seq == "stdlib_back":
       stack_test = []

       for i in range(R):
           for k in range(1, S):
               stack_test.append(k)
           for k in range(1, S):
               s += stack_test.pop()

   elif arg_seq == "stdlib_front":
       stack_test = []

       for i in range(R):
           for k in range(1, S):
               stack_test.insert(0, k)
           for k in range(1, S):
               s += stack_test.pop(0)

   elif arg_seq == "container_deque": # right
       deque_test = deque()

       for i in range(R):
           for k in range(1, S):
               deque_test.append(k)
           for _ in range(1, S):
               s += deque_test.pop()

   elif arg_seq == "debug_stdlib":
       stack_test = []

       for i in range(R):
           for k in range(1, S):
               stack_test.append(k)
               print(stack_test)
           for _ in range(1, S):
               stack_test.pop()
               print(stack_test)

elif arg_test == "concat":
    # concatenation of two sequences

    if arg_seq == "debug":
       s1 = Esek.create_empty()
       s2 = Esek.create_empty()
       for k in range(1, S):
           s1.push_back(k)
           s2.push_back(k + S - 1)
       s1.print_general(print_item)
       s2.print_general(print_item)
       s1.concat_back(s2)
       print("=== CONCAT ===")
       s1.print_general(print_item)

    if arg_seq == "esek":
        s2 = Esek.create_empty()
        t1 = time.time()
        for k in range(R):
            t2 = time.time()
            for j in range(1, S):
                s1 = Esek.create_empty()
                s1.push_back(j)
                s2.push_back(j + S - 1)
            # remove time caused by recreating the sequences
            tminus += time.time() - t2
            s1.concat_back(s2)
        # TODO: ajouter à la fin une ligne du type "s = s1.size()", idem dans l'autre test

    if arg_seq == "stdlib":
        s1 = []
        s2 = []
        for k in range(1, S):
            s1.append(k)
            s2.append(k + S - 1)
        t1 = time.time()
        for k in range(R):
            s3 = s1 + s2

elif arg_test == "flatten":

    if arg_seq == "esek":
        seqs = Esek.create_empty()
        for i in range(R):
            seqs.push_back(Esek.init(S, lambda i: i))
        result = Esek.create_empty()
        t1 = time.time()
        for i in range(R):
            result.concat_back(seqs.pop_front())
        # TODO: ajouter à la fin une ligne du type "s = result.size()", idem dans l'autre test

    if arg_seq == "stdlib":
        seqs = []
        for i in range(R):
            seqs.append([i for i in range(S)])
        result = []
        t1 = time.time()
        for i in range(R):
            result += (seqs[i])

else:
   raise ValueError("Test not found. Available tests: stack|concat|flatten")

print("exectime", time.time() - t1 - tminus)

# TODO: renommer s en result, après avoir renommer result en s dans le test "flatten".
print("result", s)
