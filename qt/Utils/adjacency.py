import math

class Adjacency():
    def __init__(self):
        self.adj = []


    def circular(self, img):
        self.adj = [0, 1, -img.xsize+1, -img.xsize, -img.xsize-1, -1, img.xsize-1, img.xsize, img.xsize+1]
    


if __name__ = "__main__":
    pass