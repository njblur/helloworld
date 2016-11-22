import numpy as np

def generate_data(size):
    _inputs = np.zeros(size)
    _labels = np.zeros(size)

    meet = False

    for i in range(size):
        x = np.random.randint(6)
        _inputs[i]=x
        if(x == 0):
            if(meet):
                _labels[i]=1
                meet = False
            else:
                meet = True
    return _inputs,_labels

size = 50000
test_size = 1000
inputs,labels = generate_data(size)

np.savetxt("_inputs",inputs)
np.savetxt("_labels",labels)

inputs,labels = generate_data(test_size)


np.savetxt("_tinputs",inputs)
np.savetxt("_tlabels",labels)
