import numpy as np
import matplotlib.pyplot as plt

def Weibull_dist(x,A,k):
    if x < 0:
        return 0
    else:
        return k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)



