# fichier pour faire des tests manuels

import chunk
import pchunk
import pstack
import view
import seq

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

    # mychunk = pchunk.Pchunk()
    # mychunk = mychunk.push_right(3)
    # mychunk = mychunk.push_left(2)
    # mychunk2 = mychunk.push_left(1)
    # mychunk = mychunk.push_left(4)
    # print('mychunk')
    # mychunk.print_general(print_item)    # [4, 2, 3]
    # print('\nmychunk2')
    # mychunk2.print_general(print_item)   # [1, 2, 3]

    # mychunk, four  = mychunk.pop_left()
    # mychunk, three = mychunk.pop_right()
    # print('\nmychunk, enlevé', four , 'à gauche et', three, 'à droite')
    # mychunk.print_general(print_item)    # [2]

    # mystack = pstack.Pstack()
    # mystack = mystack.push(1)
    # mystack = mystack.push(2)
    # mystack = mystack.push(3)
    # mystack = mystack.push(4)
    # mystack = mystack.push(5)
    # mystack = mystack.push(6)

    # print('stack')
    # mystack.print_general(print_item)

    # mystack = mystack.pop()
    # mystack = mystack.pop()
    # mystack = mystack.pop()

    # print('after pop 3 elts')
    # mystack.print_general(print_item)

    # mychunk = chunk.chunk()
    # mychunk.push_right(1)
    # mychunk.push_right(2)
    # mychunk.push_right(3)
    # mychunk.push_right(4)

    # mychunk.print_general(print_item)

    # mychunk.pop_left()
    # print("get relatif 1er elt = ", mychunk.get(0))
    # print("get absolu 1er elt = ", mychunk.get_absolute(0))

    myseq = seq.Seq()
    for i in range(25):
        myseq.push_front(i)
    myseq.print_general(print_item)

def print_item(item):
    print(item, end="")

main()