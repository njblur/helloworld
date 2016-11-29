import tensorflow as tf
import numpy as np
import SkReader

batch_size = 1
steps = 7
features = 5
hidden_size = 10
inputs = tf.placeholder(shape=[batch_size,steps,features],dtype=tf.float32)
# inputs = tf.nn.dropout(inputs,0.8)
labels = tf.placeholder(shape=[batch_size,1],dtype=tf.float32)
cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_size)
# cell = tf.nn.rnn_cell.DropoutWrapper(cell)
init_state = cell.zero_state(batch_size,dtype=tf.float32)
state = init_state

outs = []

for step in range(steps):
    if(step > 0):
        tf.get_variable_scope().reuse_variables()
    [cellout,state] = cell(inputs[:,step,:],state)
    outs.append(cellout)
output = tf.concat(1,outs)
weights = tf.Variable(tf.zeros([hidden_size*steps,1]))
bias = tf.Variable([0.0])
values = tf.matmul(output,weights)
values = values + bias
# loss = tf.squared_difference(values,labels)
loss = values-labels
loss = loss*loss

# mean = tf.reduce_all(loss)
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)


with tf.Session() as sess:
    reader = SkReader.SkReader("000001.csv",batch_size=batch_size,steps=steps,begin='2015-01-01')
   
    x2 = reader.tail_steps()
    tf.initialize_all_variables().run()
    for j in range(3):
        istate = sess.run(init_state)
        reader.reset_batch()
        for i in range(reader.data_len/reader.batch_size-steps):
            x,y = reader.next_batch()
            r,istate = sess.run([train_step,state],feed_dict={inputs:x,labels:y.reshape([-1,1]),init_state:istate})

    w=weights.eval()
    b=bias.eval()
    istate = sess.run(init_state)
    v,istate = sess.run([values,state],feed_dict={inputs:x2,init_state:istate})
    print(x2)

    print(v)




