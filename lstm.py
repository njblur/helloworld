import time

import numpy as np
import tensorflow as tf

_inputs = np.loadtxt("_inputs").reshape([-1,1])
_labels = np.loadtxt("_labels").reshape([-1,1])

num_samples = len(_inputs)

batch_size = 1
hidden_size = 100

lstm_cell = tf.nn.rnn_cell.LSTMCell(hidden_size)
lstm_drop = tf.nn.rnn_cell.DropoutWrapper(lstm_cell,output_keep_prob=1.0)
initial_state = lstm_drop.zero_state(batch_size, tf.float32)
test_state = lstm_cell.zero_state(1, tf.float32)
inputs = tf.placeholder(dtype = tf.float32,shape=[None,1])
labels = tf.placeholder(dtype = tf.float32,shape=[None,1])

inputs_drop = tf.nn.dropout(inputs,1.0)

state = initial_state
(cell_output, state) = lstm_drop(inputs_drop, state)

weights = tf.Variable(tf.zeros([hidden_size,1]))
bias = tf.Variable(3.0)

max = tf.matmul(cell_output,weights)+bias

active = tf.sigmoid(max)

tstate = test_state
tf.get_variable_scope().reuse_variables()
(t_output, tstate) = lstm_cell(inputs, tstate)

tmax = tf.matmul(t_output,weights)+bias

tactive = tf.sigmoid(tmax)

loss = -labels*tf.log(active)-(1-labels)*tf.log(1-active)

loss = tf.reduce_sum(loss,1)

loss = tf.reduce_mean(loss)

min = tf.train.AdadeltaOptimizer(1.0).minimize(loss)

with tf.Session() as sess:
    tf.initialize_all_variables().run()
    zstate = sess.run(initial_state)
    istate = zstate
    loops = num_samples//batch_size - 1000
    for j in range(loops):
        i = j % loops
        r,m,istate = sess.run([loss,min,state],feed_dict={inputs:_inputs[i*batch_size:(i+1)*batch_size,:],labels:_labels[i*batch_size:(i+1)*batch_size,:],initial_state:istate})
        if(_labels[i][0] == 1):
            istate = zstate
    print(r)

    zstate = sess.run(test_state)
    istate = zstate
    # test = [1,1,2,1,3,1,1,0,2,1,0,1,1,0,2,3,0,1,3]
    test = np.loadtxt("_inputs")
    target = np.loadtxt("_labels")
    start = -1090
    len = 15
    data = test[start:start+len]
    t = target[start:start+len]
    print(data)
    print(t)

    for t in data:
        r,istate = sess.run([tactive,tstate],feed_dict={inputs:[[t]],test_state:istate})
        print(r)
        if(r > 0.5):
            print("reset state")
            istate = zstate

