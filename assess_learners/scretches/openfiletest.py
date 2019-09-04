import numpy as np

import sys

f = open(sys.argv[1], 'r')
# print f
# print type(f)
data = np.genfromtxt(f,delimiter=',')
if sys.argv[1] == 'istanbul.csv':
    data = data[1:, 1:]