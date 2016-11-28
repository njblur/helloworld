import tensorflow as tf
import numpy as np
import SkReader

batch_size = 100
steps = 5
features = 5
hidden_size = 60
inputs = tf.placeholder(shape=[batch_size,steps,features],dtype=tf.float32)
labels = tf.placeholder(shape=[batch_size],dtype=tf.float32)
cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_size)
init_state = cell.zero_state(batch_size,dtype=tf.float32)
state = init_state

outs = []

for step in range(steps):
    if(step > 0):
        tf.get_variable_scope().reuse_variables()
    [cellout,state] = cell(inputs[:,step,:],state)
    outs.append(cellout)
flt_outs = tf.concat(1,outs)
output = tf.reshape(flt_outs,[-1,hidden_size])


with tf.Session() as sess:
    reader = SkReader.SkReader("sh000001.csv")
    x,y = reader.next_batch()
    tf.initialize_all_variables().run()
    r = sess.run(output,feed_dict={inputs:x,labels:y})
    print(r.shape)