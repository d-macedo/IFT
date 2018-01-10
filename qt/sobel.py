import numpy
import scipy
from scipy import ndimage

im = scipy.misc.imread("aaa.png")
im = im.astype('int32')
dx = ndimage.sobel(im, 0)  # derivativa horizontal
dy = ndimage.sobel(im, 1)  # derivativa vertical
mag = numpy.hypot(dx, dy)  # magnitude
mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
scipy.misc.imsave('sobel.jpg', mag)