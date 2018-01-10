from skimage import io
from skimage.filter import sobel
from skimage.filter import threshold_otsu
import numpy as np
from scipy import ndimage
import pdb

from scipy import ndimage

from GQueue import GQueue

np.set_printoptions(threshold='nan')


WHITE = 0
GREY = 1
BLACK = 2


# def sobel(img):
#     Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
#     Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

#     # borders are set to constant value 0.0
#     Gx = ndimage.convolve(img, Kx, mode="constant", cval=0.0)
#     Gy = ndimage.convolve(img, Ky, mode="constant", cval=0.0)

#     return np.sqrt((np.square(Gx) + np.square(Gy))).astype("int")



def save_normalize(grad, out_path):
    factor = 255.0 / np.max(grad)
    out = (grad * factor).astype("int")
    io.imsave(out_path, out)


def is_valid(img, coord):
    x, y = coord
    return (x >= 0 and x < img.shape[0]) and (y >= 0 and y < img.shape[1])


def watershed(img, obj_seeds, bg_seeds):
    adj8 = [(0, 0), (-1,-1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1),
            (0, 1), (1, 1)]

    grad = sobel(img)
    # io.imsave("grad.png", grad)
    grad = grad * 255
    grad = grad.astype(int)
    path_val = np.ones(grad.shape) * float("inf")
    label_img = np.zeros(grad.shape)
    color = np.zeros(grad.shape) # WHITE = 0
    max_value = np.max(grad)

    # path_val = np.ones(img.shape) * float("inf")
    # label_img = np.zeros(img.shape)
    # color = np.zeros(img.shape) # WHITE = 0
    # max_value = 256

    Q = GQueue(max_value)

    for p in bg_seeds:
        color[p] = GREY
        label_img[p] = 0
        path_val[p] = 0
        Q.insert(p, grad[p])
        # Q.insert(p, 0)
    
    for p in obj_seeds:
        color[p] = GREY # GREY means that the pixel is inside the queue
        label_img[p] = 1
        path_val[p] = 0
        Q.insert((p), grad[p])
        # Q.insert((p), 0)


    # put the seeds into GQueue

    
    c_cursor = Q.cursor
    c = 0
    while not Q.is_empty():

        # if Q.cursor != c_cursor:
        #     print str(Q.cursor) + " " + str(c_cursor) + " " + str(c)
        #     c_cursor = Q.cursor
        print "before: " + str(Q.cursor) + " " + str(Q.n_elems) + " " + str(len(Q.queue[12])) + " " + str(c)

        p = Q.remove()
        # print "after: " + str(Q.cursor) + " " + str(Q.n_elems) + " " + str(len(Q.queue[12])) + " " + str(c)
        
               

        if p == None :
            Q.cursor += 1
            Q.cursor = Q.cursor % len(Q.queue)
            continue


        c += 1

        color[p] = BLACK # pixel p has the min path cost


        # for each adjacency to p
        for dx, dy in adj8:
            q = (p[0] + dx, p[1] + dy)

            if is_valid(grad, q): 
            # if is_valid(img, q):
                # the cost of the path from the root until pixel q through p
                # is the max between the cost of the path until p and the cost
                # of the edge pq
                tmp = int(max(path_val[p], grad[q]))

                # distance = abs(img[p] - img[q])
                # tmp = min(path_val[p] + distance , img[q])

                # print str(p[0]) + " " + str(p[1]) + " | " + str(q[0]) + " " + str(q[1]) + " | " + str(path_val[p]) + " " + str(grad[q]) + " | " + str(path_val[q])
                


                # if the cost offered is less than the current cost from a
                # path from the root to q, then the pixel p "conquers" q
                # if tmp < path_val[q]:
                if tmp < path_val[q]:

                    path_val[q] = tmp

                    label_img[q] = label_img[p]
                    
                    # only WHITE or GREY colors enter in this if

                    # q never entered into queue
                    # if color[q] == GREY:
                    #     print "entrei efgkfhgwfkhgwefkgrhfehkgfekghrhgkfehg"
                    #     Q.remove_elem(q, path_val[q])
                        

                    # label from pixl p is propagates to q
                    # label_img[q] = label_img[p]
                    # path_val[q] = tmp
                    # print "inserted at " + str(tmp) + " | " + str(Q.cursor) + " | " + str(c) 
                    # if tmp != Q.cursor:
                    #     # print str(tmp) + " temp"
                    if color[q] == WHITE:
                        color[q] = GREY
                        print int(path_val[q])
                        Q.insert(q, int(path_val[q]))

        # break
                
    # for y in range(0, len(img)):
    #     for x in range(0, len(img[0])):
    #         print str(x) + " " + str(y) + " " + str(label_img[y,x]) 

    return label_img











# def main():
#     img = io.imread("square2.pgm")

#     bg_seeds = [(10, 10)]
#     obj_seeds = [(58, 58)]

#     seg = watershed(img, obj_seeds, bg_seeds)

#     io.imsave("seg.pgm", seg)





# if __name__ == "__main__":
#     main()

