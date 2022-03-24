## Open CV examples and tutorial
import numpy as np
import cv2
from matplotlib import pyplot as plt

## Load Image
img = cv2.imread('IRES_Image.png', 0)

## Display image
# cv2.imshow('IRES', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

## using matplotlib to show image
# plt.imshow(img, cmap='gray', interpolation='bicubic')
# plt.xticks([]), plt.yticks([]) ## hides tick values on x and y axis
# plt.show()

print(img.shape)
print(img.size)
print(img.dtype)

## split image to channels of blue, green, red (costly in time)
# b,g,r = cv2.split(img)
# print(b.shape)
# cv2.imshow('blue', b)
# cv2.imshow('green', g)
# cv2.imshow('red', r)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

## 2D convolution (Image Filtering) with kernel
# kernel = np.ones((2,2),np.float32)/4
# dst = cv2.filter2D(img, -1, kernel)
# cv2.imshow('filtered', dst)

## bilateral filtering (keeps edges)
# blur = cv2.bilateralFilter(img, 9, 75, 75)
# cv2.imshow('blur', blur)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

## Histogramming
hist = cv2.calcHist([img],[0],None, [256],[0,256])
plt.subplot(121), plt.imshow(img, 'gray')
plt.subplot(122), plt.plot(hist)
plt.show()