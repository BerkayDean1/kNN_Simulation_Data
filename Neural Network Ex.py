## Neural Network Ex
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils, to_categorical
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
import numpy as np

## Load Dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

print("X_train shape", X_train.shape)
print("y_train shape", y_train.shape)
print("X_test shape", X_test.shape)
print("y_test shape", y_test.shape)

## plots first nine in dataset
for i in range(9):
	# define subplot
	plt.subplot(330 + 1 + i)
	# plot raw pixel data
	plt.imshow(X_train[i], cmap=plt.get_cmap('gray'))
plt.show()

## can reshape dataset with single color channel
classes = np.unique(y_train)
nClasses = len(classes)
print('Total num of Outputs: ', nClasses)
print('Output Classes: ', classes)