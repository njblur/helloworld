import sys
import tensorflow as tf
import numpy as np
import Image
import mnist
index = 100
print sys.argv
if(len(sys.argv)>1):
	index = int(sys.argv[1])

data_sets = mnist.read_data_sets("data")
train = data_sets.train
images = train.images
labels = train.labels
image = Image.new('L',(28,28))
for idx in range(10000):
	if (labels[idx] == 0):
		break
else:
	idx = index

img = images[idx]
newimg = img.reshape([28,28])
for y in range(newimg.shape[0]):
	for x in range(newimg.shape[1]):
			if(newimg[y][x] > 0):
				image.putpixel((x,y),100)
			else:
				image.putpixel((x,y),0)
image.show()
print "label for {} is {} ".format(idx , labels[idx])
