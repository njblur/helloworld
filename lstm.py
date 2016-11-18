import time

import numpy as np
import tensorflow as tf

batch_size = 1
size = 2

lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(100, forget_bias=0.0, state_is_tuple=True)
initial_state = lstm_cell.zero_state(batch_size, tf.float32)
inputs = tf.placeholder(dtype = tf.float32,shape=[1,2])

outputs = []
state = initial_state
(cell_output, state) = lstm_cell(inputs, state)

with tf.Session() as sess:
    tf.initialize_all_variables().run()
    r = sess.run(cell_output,feed_dict={inputs:[[1,5]]})
    print(r)
