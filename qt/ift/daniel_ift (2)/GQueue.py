import numpy as np
import pdb


# class Node:
#     def __init__(self):
#         self.prev = -1
#         self.next = -1
#     def __repr__(self):
#         return "(%d, %d)" % (self.prev, self.next)
#         self.next = -1
#     def __str__(self):
#         return "(%d, %d)" % (self.prev, self.next)


class GQueue:
    def __init__(self, max_cost):
        self.queue = []
        for _ in range(max_cost+1):
            self.queue.append([])
        self.cursor = -1
        self.n_elems = 0

    def is_empty(self):
        return self.n_elems == 0


    def find_coord(self, coord, bucket):
        for bucket_coord, idx in enumerate(self.queue[bucket]):
            if bucket_coord == coord:
                return idx
        return -1 # it did not find that


    # coord = (i,j)
    # cost is the bucket where the coord will be inserted
    def insert(self, coord, cost):
        if self.is_empty():
            self.cursor = cost

        self.queue[cost].append(coord)
        self.n_elems += 1


    def remove(self):
        cursor = None

        # if the queue is not empty, it means that the cursor is "pointing" to
        # a valid bucket
        if not self.is_empty():
            coord = self.queue[self.cursor].pop(0)
            self.n_elems -= 1

            # bucket [self.cursor] is empty, then we need to find the next bucket with
            # elements to move self.cursor
            if not self.queue[self.cursor]:
                if self.is_empty():
                    self.cursor = -1
                else: # find the next bucket with elements
                    for bucket in range(self.cursor+1, len(self.queue)):
                        if self.queue[bucket]:
                            self.cursor = bucket
                            break

        return coord



    # remove the element coord in bucket cost
    def remove_elem(self, coord, cost):
        if coord in self.queue[cost]:
            self.queue[cost].remove(coord)












