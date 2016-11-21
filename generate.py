import numpy as np

size = 50000

_inputs = np.zeros(size)
_labels = np.zeros(size)

meet = False

for i in range(size):
    x = np.random.randint(4)
    _inputs[i]=x
    if(x == 0):
        if(meet):
            _labels[i]=1
            meet = False
        else:
            meet = True

np.savetxt("_inputs",_inputs)
np.savetxt("_labels",_labels)
