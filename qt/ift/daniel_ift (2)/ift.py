from skimage import io
import numpy as np
from scipy import ndimage
import pdb

from scipy import ndimage

from GQueue import GQueue


WHITE = 0
GREY = 1
BLACK = 2


def sobel(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # borders are set to constant value 0.0
    Gx = ndimage.convolve(img, Kx, mode="constant", cval=0.0)
    Gy = ndimage.convolve(img, Ky, mode="constant", cval=0.0)

    return np.sqrt((np.square(Gx) + np.square(Gy))).astype("int")



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
    path_val = np.ones(grad.shape) * float("inf")

    # predecessor map - it will be the final segmentation
    label_img = np.zeros(grad.shape)
    color = np.zeros(grad.shape) # WHITE = 0

    Q = GQueue(np.max(grad))

    # put the seeds into GQueue
    for p in obj_seeds:
        color[p] = GREY # GREY means that the pixel is inside the queue
        label_img[p] = 1
        path_val[p] = 0
        Q.insert((p), grad[p])

    for p in bg_seeds:
        color[p] = GREY
        label_img[p] = 0
        path_val[p] = 0
        Q.insert(p, grad[p])


    while not Q.is_empty():
        p = Q.remove()
        color[p] = BLACK # pixel p has the min path cost


        # for each adjacency to p
        for dx, dy in adj8:
            q = (p[0] + dx, p[1] + dy)

            if is_valid(grad, q):
                # the cost of the path from the root until pixel q through p
                # is the max between the cost of the path until p and the cost
                # of the edge pq
                tmp = int(max(path_val[p], grad[q]))


                # if the cost offered is less than the current cost from a
                # path from the root to q, then the pixel p "conquers" q
                if tmp < path_val[q]:
                    # only WHITE or GREY colors enter in this if

                    # q never entered into queue
                    if color[q] == GREY:
                        Q.remove_elem(q, path_val[q])

                    # label from pixl p is propagates to q
                    label_img[q] = label_img[p]
                    path_val[q] = tmp
                    Q.insert(q, tmp)

    return label_img











def main():
    img = io.imread("square2.pgm")

    bg_seeds = [(10, 10)]
    obj_seeds = [(58, 58)]

    seg = watershed(img, obj_seeds, bg_seeds)

    io.imsave("seg.pgm", seg)





if __name__ == "__main__":
    main()

