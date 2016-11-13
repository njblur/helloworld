import tensorflow as tf
import time
import sys

rank = 3000
#with tf.device("/cpu:0"):
a = tf.range(rank**2)
aa = tf.reshape(a,[rank,rank])
b = tf.range(rank**2)
bb = tf.reshape(a,[rank,rank])
c = tf.matmul(aa,bb)
i = tf.matrix_inverse(tf.to_float(c))
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
	start = time.clock()
	print sess.run(i)
	print time.clock() - start
