import sys
import math
import tensorflow as tf
v = tf.Variable(tf.zeros([1,2]))
x = tf.placeholder(tf.float32,[2,None])
y = tf.placeholder(tf.float32,[None])
yc = tf.matmul(v,x)
loss = tf.squared_difference(y,yc)
trainer = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
init = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init)
    for i in range(1000):
        trainer.run(feed_dict={x:[[2, 1, 4], [5, 1, 7]],y:[19, 5, 29]},session=sess)
       
    p = v.eval()
    leg1 = int(p[0][0]+0.5)
    leg2 = int(p[0][1]+0.5)
    print("animal one has {} legs and animal2 has {} legs".format(leg1,leg2))
