from src.utility import Weibull_dist
import numpy as np
import matplotlib.pyplot as plt

k = 2.85
A = 10
x = np.linspace(0, 30, 1000, endpoint=True)
y = [Weibull_dist(i, A, k) for i in x]


plt.plot(x, y, '.')
plt.show()

