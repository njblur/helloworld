import sys
import time
import tensorflow as tf
import numpy as np
import mnist


batch_size = 100
classnum = 10
width = 28
height = 28
learning_rate = 0.2

test_index = 88


def inflat_labels(labels):
    labels_inflat = np.zeros([batch_size,classnum])
    indices = np.arange(labels_inflat.shape[0])*labels_inflat.shape[1] + labels
    labels_inflat.flat[indices] = 1
    return labels_inflat



data_sets = mnist.read_data_sets("data")

train = data_sets.train
test = data_sets.test
test_size = test.num_examples//10

x = tf.placeholder(shape=[batch_size,width,height,1],dtype=tf.float32)
xv = tf.placeholder(shape=[test_size,width,height,1],dtype=tf.float32)

y_ = tf.placeholder(shape=[batch_size],dtype=tf.int32)

con_weights1 = tf.Variable(tf.truncated_normal(shape=[5,5,1,32],stddev=0.1))
conv_bias1 = tf.Variable(tf.zeros([32]))

con_weights2 = tf.Variable(tf.truncated_normal(shape=[5,5,32,64],stddev=0.1))
conv_bias2 = tf.Variable(tf.zeros([64]))


conv1 = tf.nn.conv2d(x,con_weights1,strides=[1,1,1,1],padding="SAME")
conv1bias = tf.nn.bias_add(conv1,conv_bias1)
relu = tf.nn.relu(conv1bias)
pool = tf.nn.max_pool(relu,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")

conv2 = tf.nn.conv2d(pool,con_weights2,strides=[1,1,1,1],padding="SAME")
conv2bias = tf.nn.bias_add(conv2,conv_bias2)
relu2 = tf.nn.relu(conv2bias)
pool2 = tf.nn.max_pool(relu2,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")

shape = pool2.get_shape().as_list()

features = shape[1]*shape[2]*shape[3]
reshape = tf.reshape(pool2,[shape[0],features])
fc1_weights = tf.Variable(tf.truncated_normal([features,classnum],stddev=0.1))
fc1_bias = tf.Variable(tf.constant(0.1,shape=[classnum]))

out = tf.matmul(reshape,fc1_weights)+fc1_bias



entrop=tf.nn.sparse_softmax_cross_entropy_with_logits(out, y_, name=None)

mean = tf.reduce_mean(entrop)

regu = tf.nn.l2_loss(fc1_weights) + tf.nn.l2_loss(fc1_bias)

mean += 0.0005*regu

train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(mean)

#test 
conv1t = tf.nn.conv2d(xv,con_weights1,strides=[1,1,1,1],padding="SAME")
conv1biast = tf.nn.bias_add(conv1t,conv_bias1)
relut = tf.nn.relu(conv1biast)
poolt = tf.nn.max_pool(relut,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
conv2t = tf.nn.conv2d(poolt,con_weights2,strides=[1,1,1,1],padding="SAME")
conv2biast = tf.nn.bias_add(conv2t,conv_bias2)
relu2t = tf.nn.relu(conv2biast)
pool2t = tf.nn.max_pool(relu2t,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME") 
shapet = pool2t.get_shape().as_list()

featurest = shapet[1]*shapet[2]*shapet[3]
reshapet = tf.reshape(pool2t,[shapet[0],featurest])

outt = tf.matmul(reshapet,fc1_weights)+fc1_bias

out_max = tf.arg_max(outt,1)

iteration = train.num_examples/batch_size
#iteration = 1

var_init = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(var_init)
    before = time.time()
    for i in range(iteration):
        images,labels = train.next_batch(batch_size)
        images = images.reshape(batch_size,28,28,1)
        tt = sess.run(train_step,feed_dict={x:images,y_:labels})
    print time.time()-before
    v = sess.run(out_max,feed_dict={xv:test.images[0:test_size].reshape(test_size,28,28,1)})
    a=test.labels[0:test_size]
    t = v == a
    tc = t[t==True]
    print len(t)
    print len(tc)
    print len(tc)*10/len(t)

