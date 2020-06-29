import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utility import *
import matplotlib.gridspec as gridspec


# load the data
dataA = pd.read_csv('data/Fig3A.csv', sep=',')
dataB = pd.read_csv('data/Fig3B.csv', sep=',')
dataC = pd.read_csv('data/Fig3C.csv', sep=',')
dataD = pd.read_csv('data/Fig3D.csv', sep=',')
dataE = pd.read_csv('data/Fig3E.csv', sep=',')
dataF = pd.read_csv('data/Fig3F.csv', sep=',')

# generating fit
A = 7
y_predA = [power(i, 0.5, A) for i in dataA['x']]
rmsA = rms(y_predA, dataA['y'])

B = 0.65
y_predB = [power(i, 0.5, B) for i in dataB['x']]
rmsB = rms(y_predB, dataB['y'])

C = 262
y_predC = [power(i, 0.5, C) for i in dataC['x']]
rmsC = rms(y_predC, dataC['y'])

D = 0.9
y_predD = [power(i, -0.5, D) for i in dataD['x']]
rmsD = rms(y_predD, dataD['y'])

Ea = 1
Eb = 0
y_predE = [lin(i, Ea, Eb) for i in dataE['x']]
rmsE = rms(y_predE, dataE['y'])

Fa = 1
Fb = 0
y_predF = [lin(i, Fa, Fb) for i in dataF['x']]
rmsF = rms(y_predF, dataF['y'])


# config of the plot
font_size = 10
params = {'axes.labelsize': font_size,
          'axes.titlesize': font_size,
          'xtick.labelsize': font_size,
          'ytick.labelsize': font_size
          }
plt.rcParams.update(params)
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(2, 3, figure=fig)


# do the plot
p1 = fig.add_subplot(gs[0, 0])
plt.title("A")
p1.plot(dataA['x'], dataA['y'], '.')
p1.plot(dataA['x'], y_predA, '-', label='$y = 7 \cdot x^{0.5}$')
p1.text(0.5, 22, "rms residual (µm): " + f'{rmsA:.2}', fontsize=font_size)
plt.legend()
p1.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p1.set_xlabel('Diffusion coefficient ($µm^2/s$)', fontsize=font_size)
p1.legend()

p2 = fig.add_subplot(gs[0, 1])
plt.title("B")
p2.plot(dataB['x'], dataB['y'], '.')
p2.plot(dataB['x'], y_predB, '-', label='$y = 0.65 \cdot x^{0.5}$')
p2.text(200, 25, "rms residual (µm): " + f'{rmsB:.2}', fontsize=font_size)
p2.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p2.set_xlabel('Number of motors', fontsize=font_size)
p2.legend()

p3 = fig.add_subplot(gs[0, 2])
plt.title("C")
p3.plot(dataC['x'], dataC['y'], '.')
p3.plot(dataC['x'], y_predC, '-', label='$y = 262 \cdot x^{0.5}$')
p3.text(0.002, 25, "rms residual (µm): " + f'{rmsC:.2}', fontsize=font_size)
p3.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p3.set_xlabel('Length increase per motor (µm)', fontsize=font_size)
p3.legend()

p4 = fig.add_subplot(gs[1, 0])
plt.title("D")
p4.plot(dataD['x'], dataD['y'], '.')
p4.plot(dataD['x'], y_predD, '-', label='$y = 0.9 \cdot x^{-0.5}$')
p4.text(0.02, 25, "rms residual (µm): " + f'{rmsD:.2}', fontsize=font_size)
p4.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p4.set_xlabel('Decay rate (µm/s)', fontsize=font_size)
p4.legend()

p5 = fig.add_subplot(gs[1, 1])
plt.title("E")
p5.plot(dataE['x'], dataE['y'], '.')
p5.plot(dataE['x'], y_predE, '-', label='$y = x$')
p5.text(5, 25, "rms residual (µm): " + f'{rmsE:.2}', fontsize=font_size)
p5.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p5.set_xlabel('Predicted length from eq(1) (µm)', fontsize=font_size)
p5.legend()

p6 = fig.add_subplot(gs[1, 2])
plt.title("F")
p6.plot(dataF['x'], dataF['y'], '.')
p6.plot(dataF['x'], y_predF, '-', label='$y = x$')
p6.text(5, 30, "rms residual (µm): " + f'{rmsF:.2}', fontsize=font_size)
p6.set_ylabel('Steady-state flagellar length (µm)', fontsize=font_size)
p6.set_xlabel('Predicted length from eq(1) (µm)', fontsize=font_size)
p6.legend()

plt.show()
