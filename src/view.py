class View:

    def __init__(self, head = 0, size = 0):
        self.seg_head = head
        self.seg_size = size

    # override == operator
    def __eq__(self, other): 
        return (self.seg_head == other.seg_head and
                self.seg_size == other.seg_size)
    