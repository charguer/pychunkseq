# fichier pour faire des tests manuels

FRONT = __import__('direction').Direction.FRONT
BACK = __import__('direction').Direction.BACK

import echunk
import schunk
import view
import esek
from esek import Esek

echunk.set_capacity(8)

def main():
    # Test echunk push & pop
    print("### Test echunk push and pop")
    mychunk = echunk.Echunk()
    mychunk.push_back(2)
    mychunk.push_back(3)
    mychunk.push_front(1)
    mychunk.print_general(print_item)
    x = mychunk.pop_front()
    y = mychunk.pop_back()
    mychunk.print_general(print_item)
    print("pop_front =", x, "ok" if x == 1 else "not ok")
    print("pop_back =", y, "ok" if y == 3 else "not ok")
    print("")
    
    # Test schunk push and pop
    print("### Test schunk with push_back")
    myschunk = schunk.Schunk()
    myschunk = myschunk.push_back(2)
    myschunk2 = myschunk.push_back(3)
    myschunk = myschunk.push_back(4)
    print("myschunk = ", end="")
    myschunk.print_general(print_item)    # [2, 4]
    print("myschunk2 = ", end="")
    myschunk2.print_general(print_item)   # [2, 3]
    print("concat = ", end="")
    myconcat = myschunk.concat(myschunk2)
    myconcat.print_general(print_item)   # [2, 4, 2, 3]
    print("")

    print("### Test schunk push_back and push_front")
    myschunk3 = schunk.Schunk()
    myschunk3 = myschunk3.push_back(3)
    myschunk3 = myschunk3.push_front(2)
    myschunk4 = myschunk3.push_front(1)
    myschunk3 = myschunk3.push_front(4)
    print("myschunk3 = ", end="")
    myschunk3.print_general(print_item)    # [4, 2, 3]
    print("myschunk4 = ", end="")
    myschunk4.print_general(print_item)   # [1, 2, 3]
    print("")

    print("### Test schunk pop front and back")
    myschunk3, four  = myschunk3.pop_front()
    myschunk3, three = myschunk3.pop_back()
    print("myschunk3, enlevé", four , "à gauche et", three, "à droite")
    myschunk3.print_general(print_item)    # [2]
    print("")

    print("### Test get echunk")
    mychunk2 = echunk.Echunk()
    mychunk2.push_back(1)
    mychunk2.push_back(2)
    mychunk2.push_back(3)
    mychunk2.push_back(4)
    mychunk2.print_general(print_item)
    print("get elt index 1 = ", mychunk2[1])
    print("")

    # HERE: change value for testing 
    esek_size = 10
    print("### Test esek push front & back")
    myseq = Esek.create_empty()
    for i in reversed(range(esek_size)):
        myseq.push_front(i)
    for i in range(esek_size):
        myseq.push_back(i + esek_size)
    myseq.print_general(print_item)
    print("")

    print("--- Popping front and back")
    myseq.pop_front()
    myseq.pop_back()
    myseq.print_general(print_item)
    print("")

    # print("### Test esek pop front & back")
    # for i in range(5):
    #     myseq.pop_front()
    #     myseq.pop_back()
    # myseq.print_general(print_item)
    # print("")

    print("### Transform into ssek")
    myssek = esek.esek_to_ssek(myseq)
    myssek.print_general(print_item)
    print("-- pop_front and pop_back elements")
    myssek, x = myssek.pop_front(myssek.version_max)
    myssek, x = myssek.pop_back(myssek.version_max)
    myssek.print_general(print_item)
    print("-- transforming into esek")
    myseq = esek.ssek_to_esek(myssek)
    myseq.print_general(print_item)


    # print("### Test esek concat")
    # print("seq1 = ", end="")
    # seq1 = Esek.create_empty()
    # for i in range(esek_size):
    #     seq1.push_back(i)
    # seq1.print_general(print_item)
    # print("seq2 = ", end="")
    # seq2 = Esek.create_empty()
    # for i in range(esek_size):
    #     seq2.push_back(i + esek_size)
    # seq2.print_general(print_item)

    # print("Concatenation...")
    # seq1.concat_back(seq2)
    # print("seq1 = ", end="")
    # seq1.print_general(print_item)
    # print("seq2 = ", end="")
    # seq2.print_general(print_item)
    # print("")

    # print("### Test reverse sequence")
    # myseq = esek.Esek()
    # for i in range(esek_size):
    #     myseq.push_back(i + 1)
    # print("seq1 = ", end="")
    # myseq.print_general(print_item)
    # print("seq1.rev()")
    # myseq.rev()
    # print("seq1 = ", end="")
    # myseq.print_general(print_item)
    # myseq.pop_front()
    # print("pop front")
    # print("seq1 = ", end="")
    # myseq.print_general(print_item)
    # print("pop back")
    # print("seq1 = ", end="")
    # myseq.pop_back()
    # myseq.print_general(print_item)
    # print("")

    from ssek import Ssek
    ssek_size = 10
    print("")
    print("### Test ssek push front & back")
    myssek = Ssek.create_empty()
    for i in reversed(range(ssek_size)):
        myssek = myssek.push_front(i)
    for i in range(ssek_size):
        myssek = myssek.push_back(ssek_size + i)
    myssek.print_general(print_item)
    myssek2 = myssek.push_front(100)
    myssek = myssek.push_front(999)
    print("myssek2 = myssek.push_front(100)")
    myssek2.print_general(print_item)
    print("myssek = myssek.push_front(999)")
    myssek.print_general(print_item)
    print("myssek.pop_front()")
    myssek, x = myssek.pop_front()
    myssek.print_general(print_item)
    print("popped elt =", x)
    print("myssek.pop_back()")
    myssek, x = myssek.pop_back()
    myssek.print_general(print_item)
    print("popped elt =", x)
    

def print_item(item):
    print(item, end="")
    

main()