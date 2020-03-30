import pchunk

class Pstack:

    def __init__(self):
        self.head = pchunk.Pchunk()
        self.tail = [] # a list of pchunks

    # TODO: verifier fonctionnement (return self?)
    def push(self, item):
        if self.head.is_full():
            self.tail.append(self.head) # TODO : 
            self.head = pchunk.Pchunk()
        self.head = self.head.push('back', item)
        return self # return Pstack(new_head, new_tail)

        # TODO: implémenter le module : https://dbader.org/blog/functional-linked-lists-in-python
        #   nil
        #   cons(x, l)
        #   head(l)  tail(l)

        #   if is_empty(l) then ..
        #   else 
        #       (x,l') = uncons(l)
        #       ...

    # TODO: verifier valeur de retour, (renvoyer elt? persistent?)
    def pop(self):
        self.head = self.head.pop_back()
        if (self.head.is_empty()):
            self.head = self.tail.pop()
        return self
      # 

      # (x, new_head) = self.head.pop()
      # if new_head.is_empty()
      #    if self.tail.is_empty()
      #        new_tail = tail
      #    else
      #        (new_head, new_tail) = self.tail.uncons()
      #
      # TODO return (x, Pstack(new_head, new_tail) )

    def print_general(self, print_item):
        print("{", end = "")
        self.head.print_general(print_item)
        for i in self.tail:
            i.print_general(print_item)
            print(", ", end = "")
        print("}")
