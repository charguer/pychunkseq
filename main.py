# fichier pour faire des tests manuels

import chunk
import pchunk

def main():
    # mychunk = chunk.chunk()
    # mychunk.push_left(2)
    # mychunk.push_left(3)
    # mychunk.pop_right()
    # mychunk.print_general(print)
    
    # mychunk = pchunk.Pchunk()
    # mychunk = mychunk.push_right(2)
    # mychunk2 = mychunk.push_right(3)
    # mychunk = mychunk.push_right(4)
    # print('mychunk')
    # mychunk.print_general(print)    # [2, 4]
    # print('\nmychunk2')
    # mychunk2.print_general(print)   # [2, 3]

    mychunk = pchunk.Pchunk()
    mychunk = mychunk.push_right(3)
    mychunk = mychunk.push_left(2)
    mychunk2 = mychunk.push_left(1)
    mychunk = mychunk.push_left(4)
    print('mychunk')
    mychunk.print_general(print_item)    # [4, 2, 3]
    print('\nmychunk2')
    mychunk2.print_general(print_item)   # [1, 2, 3]

    mychunk = mychunk.pop_left()
    mychunk = mychunk.pop_right()
    print('\nmychunk')
    mychunk.print_general(print_item)    # [2]

    empty_chunk = mychunk.clear()
    print('\nempty chunk')
    empty_chunk.print_general(print_item) # []


def print_item(item):
    print(item, end="")

main()