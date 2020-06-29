import numpy as np
import matplotlib.pyplot as plt

def Weibull_dist(x,A,k):
    if x < 0:
        return 0
    else:
        #return k/A*(x/A)**(k-1)                       # failure rate
        return k/A*(x/A)**(k-1)*np.exp(-(x/A)**k)     # wikipedia
        #return (k/x)*((x/A)**k)*np.exp(-((x/A)**k))   # PDF
        # return 1 - np.exp(-(x/A)**k)                   # CDF
        # return np.exp(-(x/A)**k)                      # R
        # return A * x**k


def Gammaf(x,a,b):
    return (b**a*x**(a-1)*np.exp(-b*x))/np.math.factorial(a-1)

def power(x,p,A):
    return A*x**p
def lin(x,a,b):
    return a*x + b


def rms(y_pred, y):
    rms = 0
    for i, y_ in enumerate(y_pred):
        rms = rms + (y_ - y[i]) ** 2
    rms = rms / len(y_pred)
    rms = np.sqrt(rms)
    return rms

def sort_data(dx,dy):
    x = np.array(dx)
    indx = np.argsort(x)
    y = []
    for i in indx:
        y.append(dy[i])
    x = np.sort(x)

    return[x, y]




