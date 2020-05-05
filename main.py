# fichier pour faire des tests manuels

FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

import chunk
import pchunk
import pstack
import view
import seq

def main():
    # mychunk = chunk.chunk()
    # mychunk.push_front(2)
    # mychunk.push_front(3)
    # mychunk.pop('back')
    # mychunk.print_general(print)
    
    # mychunk = pchunk.Pchunk()
    # mychunk = mychunk.push_back(2)
    # mychunk2 = mychunk.push_back(3)
    # mychunk = mychunk.push_back(4)
    # print('mychunk')
    # mychunk.print_general(print)    # [2, 4]
    # print('\nmychunk2')
    # mychunk2.print_general(print)   # [2, 3]

    # mychunk = pchunk.Pchunk()
    # mychunk = mychunk.push_back(3)
    # mychunk = mychunk.push_front(2)
    # mychunk2 = mychunk.push_front(1)
    # mychunk = mychunk.push_front(4)
    # print('mychunk')
    # mychunk.print_general(print_item)    # [4, 2, 3]
    # print('\nmychunk2')
    # mychunk2.print_general(print_item)   # [1, 2, 3]

    # mychunk, four  = mychunk.pop('front')
    # mychunk, three = mychunk.pop('back')
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
    # mychunk.push_back(1)
    # mychunk.push_back(2)
    # mychunk.push_back(3)
    # mychunk.push_back(4)

    # mychunk.print_general(print_item)

    # mychunk.pop('front')
    # print("get relatif 1er elt = ", mychunk.get(0))
    # print("get absolu 1er elt = ", mychunk.get_absolute(0))

    # myseq = seq.Seq()
    # for i in range(25):
    #     myseq.push_front(i)
    # for i in range(10):
    #     myseq.push_back(i + 25)
    # myseq.print_general(print_item)

    # for i in range(34):
    #     myseq.pop_front()
    # print("after")
    # myseq.print_general(print_item)

    # print("====== SEQ 1")
    # seq1 = seq.Seq()
    # for i in range(13):
    #     seq1.push_back(i)
    # seq1.print_debug(print_item)

    # print("====== SEQ 2")
    # seq2 = seq.Seq()
    # for i in range(13):
    #     seq2.push_back(i + 13)
    # seq2.print_debug(print_item)

    # print("====== SEQ CONCAT")
    # seq1.concat_back(seq2)
    # seq1.print_general(print_item)

    # ============= TEST REV

    # print("===== SEQ")
    # myseq = seq.Seq()
    # for i in range(10):
    #     myseq.push_back(i + 1)
    # myseq.print_general(print_item)

    # # myseq.rev()
    # print("===== SEQ.REV()")
    # myseq.print_general(print_item)

    myseq = seq.Seq()
    for i in range(100):
        myseq.push_back(i + 1)
    myseq.print_general(print_item)

    myseq.rev()
    print("=== ITER")
    myseq.iter(BACK, print_item) # OK
    print("")


def print_item(item):
    print(item, " ", end="")
    

main()