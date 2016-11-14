from __future__ import absolute_import, division, print_function
import tensorflow as tf 
import numpy as np
holder = tf.placeholder(tf.int32,shape=None)
lm = tf.truncated_normal([2,3],stddev=0.8)
rm = tf.truncated_normal([3,2],stddev=5.0)
mm = tf.matmul(lm,rm)
im = tf.matrix_inverse(mm)
em = tf.matmul(mm,im)
v = tf.Variable(8,dtype=tf.int32)
v = tf.add(holder,v)
init = tf.initialize_all_variables()
eq = tf.equal(1,1)
f = tf.cast(eq,tf.int8)
r = tf.reduce_mean(f)
loss = tf.nn.softmax_cross_entropy_with_logits([1.0, 0,1.0],[1.0,0.0,1.0])
mean = tf.reduce_mean(loss)
result = 8
#contents = tf.read_file("rabbit.jpeg")
with open("rabbit2.jpg") as inf:
    contents = inf.read()
rabbit = tf.image.decode_jpeg(contents,channels=None)
rotate = tf.image.transpose_image(rabbit)
grey = tf.image.adjust_brightness(rotate,0.1)
encode = tf.image.encode_jpeg(grey)


with tf.Session() as sess:
    sess.run(init)
    for i in [3,4,8]:
        result = sess.run(v,feed_dict={holder:result})
        print(result)
    print(sess.run(r))
    print(r.eval())
    print(sess.run(em))
    print(sess.run(loss))
    print(sess.run(mean))
    save = sess.run(encode)
    with open("rabbit90.jpg","w") as f:
        f.write(save)
