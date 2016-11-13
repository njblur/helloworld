import sys
import tensorflow as tf
import numpy as np
import mnist

batch_size = 100
classnum = 10
width = 28
height = 28
learning_rate = 0.05

test_index = 88

def inflat_labels(labels):
    labels_inflat = np.zeros([batch_size,classnum])
    indices = np.arange(labels_inflat.shape[0])*labels_inflat.shape[1] + labels
    labels_inflat.flat[indices] = 1
    return labels_inflat



data_sets = mnist.read_data_sets("data")

weights = tf.Variable(tf.zeros([width*height,classnum]))
bias  = tf.Variable(tf.zeros([classnum]))
x = tf.placeholder(shape=[None,width*height],dtype=tf.float32)
y_ = tf.placeholder(shape=[None,classnum],dtype=tf.float32)
yt_ = tf.placeholder(shape=[None],dtype=tf.float32)
m = tf.matmul(x,weights)+bias
softmax = tf.nn.softmax(m)
log = tf.mul(-y_,tf.log(softmax))
sum = tf.reduce_sum(log,reduction_indices=[1],keep_dims=False)
mean = tf.reduce_mean(sum)
#opt = tf.train.GradientDescentOptimizer(learning_rate).minimize(mean)
opt = tf.train.AdadeltaOptimizer(learning_rate).minimize(mean)

var_init = tf.initialize_all_variables()

train = data_sets.train
test = data_sets.test

yt = tf.matmul(x,weights)+bias
out = tf.arg_max(yt,1)
correct = tf.equal(out,tf.to_int64(yt_))
right = tf.to_float(correct)
rate = tf.reduce_mean(right)


print test.labels[0:20].shape

print train.num_examples

images,labels = train.next_batch(batch_size)

with tf.Session() as sess:
    sess.run(var_init)
    print 5*train.num_examples/batch_size
    for i in range(15*train.num_examples/batch_size):
        images,labels = train.next_batch(batch_size)
        result = sess.run(opt,feed_dict={x:images,y_:inflat_labels(labels)})

    tt = sess.run(rate,feed_dict={x:test.images,yt_:test.labels})
   
print tt 


