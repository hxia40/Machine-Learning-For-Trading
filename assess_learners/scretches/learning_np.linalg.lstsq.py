import matplotlib.pyplot as plt
import numpy as np
# Fit a line, y = mx + c, through some noisy data-points:

x = np.array([0., 1., 2., 3.])
y = np.array([-1.0, 0.2, 0.9, 2.1])
# By examining the coefficients, we see that the line should have a gradient of roughly 1
# and cut the y-axis at, more or less, -1.

# We can rewrite the line equation as y = Ap, where A = [[x 1]] and p = [[m], [c]].
# Now use lstsq to solve for p:


A = np.vstack([x, np.ones(len(x))]).T
print 'showing A'
print A
print type(A)


m, c = np.linalg.lstsq(A, y)[0]
print m, c

# Plot the data along with the fitted line:


plt.plot(x, y, 'o', label='Original data', markersize=10)
plt.plot(x, m*x + c, 'r', label='Fitted line')
plt.legend()
plt.show()
